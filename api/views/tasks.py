from rest_framework.views import APIView
from rest_framework import generics
from api.models import User, Task
from api.serializers.tasks import TaskSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.db.models import Q


class TaskCreateAPI(generics.ListCreateAPIView):
    '''
        - GET 
        - Listing the tasks for the authenticated user
    '''
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        get_status =  self.request.query_params.get('status', '')
        get_priority = self.request.query_params.get('priority', '')
        sort_by = self.request.query_params.get('sort_by', '')
        search = self.request.query_params.get('search', '')
        
        tasks = Task.objects.filter(user_id=user.id)

        if search:
            tasks = Task.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))

        if get_status:
            tasks = Task.objects.filter(user_id=user.id, status=get_status)

        if get_priority:
            tasks = Task.objects.filter(user_id=user.id, priority=get_priority)
        
        if get_status and get_priority:
            tasks = Task.objects.filter(user_id=user.id, status=get_status, priority=get_priority)
        
        if sort_by:
            tasks = tasks.order_by(sort_by)

        return tasks
    
    
    def list(self, request):
        queryset = self.get_queryset()
        result_len =  queryset.count()
        serializer = TaskSerializer(queryset, many=True)
        return Response({ "status": "success", "count": result_len, "data" :serializer.data})

    def perform_create(self, serializer):
        due_date = serializer.validated_data.get('due_date')
        user = self.request.user.id
        get_user = User.objects.get(id=user)
        if due_date:
            created_at = timezone.now().date()
            if due_date < created_at:
                raise ValidationError("Due date cannot be before the creation date.")
            serializer.save(created_at=created_at, user=get_user)
            
        else:
            serializer.save(user=get_user)


class TasksAPI(APIView):

    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user_id=user)
        except Task.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        print("1")
        user = request.user.id
        snippet = self.get_object(pk, user)
        serializer = TaskSerializer(snippet)
        return Response({"status": "success" ,"data":serializer.data}, status=status.HTTP_200_OK)

    
    def put(self, request, pk, format=None):
        user = request.user.id
        task = self.get_object(pk, user)
        pre_status = Task.objects.get(id=task.id).status

        get_status = request.data.get('status', task.status)
        get_title = request.data.get("title", task.title)
        get_due = request.data.get("due_date", task.due_date)
        get_priority = request.data.get("priority", task.priority)
        get_assigned = request.data.get("assigned_to", task.assigned_to)
        print(get_due)

        if pre_status != get_status:
            if pre_status == "1" and get_status == "2":
                pass 
            elif pre_status == "2" and get_status == "3":
                pass  
            else:
                return Response({"status": "error", "msg": f"Cannot assign to status {get_status} from {pre_status}"}, status=status.HTTP_400_BAD_REQUEST)
        

        update_data = {
            'user': user,
            'title': get_title,
            'status':get_status,
            'due_date': get_due,
            'priority': get_priority,
            'assigned_to': get_assigned            
        }
        
        serializer = TaskSerializer(task, data=update_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success" ,"data":serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk, format=None):
        user = request.user.id
        task = self.get_object(pk, user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
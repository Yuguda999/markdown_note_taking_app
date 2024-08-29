from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
import markdown2
import language_tool_python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def language_tool_check(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    errors = []
    
    for match in matches:
        errors.append({
            'message': match.message,
            'offset': match.offset,
            'length': match.length,
            'context': match.context,
            'suggestions': match.replacements
        })
    
    return {'grammar_errors': errors}

class GrammarCheckView(APIView):
    def post(self, request):
        content = request.data.get('content', '')
        result = language_tool_check(content)
        return Response(result, status=status.HTTP_200_OK)

class SaveNoteView(APIView):
    def post(self, request):
        content = request.data.get('content', '')
        
        try:
            markdown2.markdown(content)
        except Exception as e:
            return Response({'error': 'Invalid markdown content'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListNotesView(APIView):
    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

class RenderNoteView(APIView):
    def get(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id)
            html_content = markdown2.markdown(note.content)
            return Response({"html": html_content})
        except Note.DoesNotExist:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

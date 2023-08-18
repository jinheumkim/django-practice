from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

nextid = 4
topics = [
{'id':1, 'title':'routing', 'body':'Routing is ..'},
{'id':2, 'title':'view', 'body':'view is ..'},
{'id':3, 'title':'model', 'body':'model is ..'}
]

# Create your views here.
def HTMLTemplate(article ,id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <form action="/delete/" method ="POST">
                    <input type ="hidden" name="id" value={id}>
                    <input type ="submit" value="Delete">
                </form>
            </li>
            <li><a href ="/update/{id}">update</li>
         '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/">django</a></h1>
        <ol>
            {ol} 
        </ol>
        {article}
        <ul>
            <li><a href="/create/">create</a></li>
            {contextUI}
        </ul>
    </body>
    </html>
    '''
def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, django
    '''
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
    global nextid
    if request.method == 'GET':
        article = '''
            <form action="/create/" method= "post">
                <p><input type ="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type = "submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method== 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newtopic = {'id':nextid, 'title':title, 'body':body}
        topics.append(newtopic)
        url = '/read/' + str(nextid)
        nextid = nextid + 1
        return redirect(url)

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article,id))

@csrf_exempt
def delete(request):
    global topics
    if request.method == "POST":
        id = request.POST['id']
        newtopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newtopics.append(topic)
        topics = newtopics
        return redirect('/')

@csrf_exempt
def update(request,id):
    global topics
    if request.method == "GET":
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method= "post">
                <p><input type ="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic['body']}</textarea></p>
                <p><input type = "submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article,id))
    elif request.method == "POST":
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')
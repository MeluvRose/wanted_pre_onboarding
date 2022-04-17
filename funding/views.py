from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Goods



# Create your views here.
def post_goods(request):
    article = 'this page for crawed funding'
    return HTMLTempleate(article)

@csrf_exempt
def create(request):
    posts = Goods.objects.all()
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><input type="text" name="publisher" placeholder="publisher"></p>
                <p><textarea name="detail" placeholder="detail"></textarea></p>
                <p><input type="text" name="goal" placeholder="goal"></p>
                <p><input type="date" name="date_limit" placeholder="YYYY-MM-DD"></p>
                <p><input type="text" name="price_per_time" placeholder="price(per_1_time)"></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTempleate(article))
    else:
        title = request.POST['title']
        publisher = request.POST['publisher']
        detail = request.POST['detail']
        goal = request.POST['goal']
        date_limit = request.POST['date_limit']
        price_per_time = request.POST['price_per_time']
        next_id = 0
        for post in posts:
            if next_id == post.id:
                next_id = next_id + 1
            else:
                break
        goods = Goods(
            id = next_id,
            title = title,
            publisher = publisher,
            detail = detail,
            goal = goal,
            date_limit = date_limit,
            price_per_time = price_per_time
        )
        goods.save()
        posts = Goods.objects.all()
        return redirect('/read/' + str(next_id))

def read(request, pk):
    posts = Goods.objects.all()
    
    article = [f'''
        <h2>{post.title}</h2>
            <ul>
                <li>Publisher : {post.publisher}</li>
                <li>Detail : {post.detail}</li>
                <li>Goal : {post.goal}</li>
                <li>Until {post.date_limit}</li>
                <li>Price : {post.price_per_time} per 1 time</li>
            </ul>
        ''' 
        for post in posts if post.id == int(pk)]
    return HTMLTempleate(*article, pk)

@csrf_exempt
def update(request, pk):
    posts = Goods.objects.get(id=pk)
    if request.method == "GET":
        selectedPost = {
            'title':posts.title,
            'publisher':posts.publisher,
            'detail':posts.detail,
            'date':posts.date_limit,
            'price':posts.price_per_time
        }
        article = f'''
            <form action="/update/{pk}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value={selectedPost['title']}></p>
                <p><input type="text" name="publisher" placeholder="publisher" value={selectedPost['publisher']}></p>
                <p><textarea name="detail" placeholder="detail">{selectedPost['detail']}</textarea></p>
                <p><input type="date" name="date_limit" placeholder="YYYY-MM-DD" value={selectedPost['date']}></p>
                <p><input type="text" name="price_per_time" placeholder="price(per_1_time)" value={selectedPost['price']}></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTempleate(article, pk))
    else:
        posts.title = request.POST['title']
        posts.publisher = request.POST['publisher']
        posts.detail = request.POST['detail']
        posts.date_limit = request.POST['date_limit']
        posts.price_per_time = request.POST['price_per_time']
        posts.save()
        return redirect(f'/read/{pk}')

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        pk = int(request.POST['id'])
        goods = Goods.objects.get(id=pk)
        goods.delete()
        return redirect('/')

def HTMLTempleate(article, id=None):
    posts = Goods.objects.all()
    contextUI = ''
    ol = ''

    if id != None:
        contextUI = f'''
            <li>
                <form action="/delete/" method="POST">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                <form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        '''
    for post in posts:
        ol += f"<li><a href='/read/{post.id}'>{post.title}</a></li>"
    return HttpResponse(f'''
    <html>
    <body>
        <h1><a href="/">CrawedFunding</a></h1>
        {article}
        <ul>
            {ol}
        </ul>
        <ul>
            <li><a href="/create/">create</a></li>
            {contextUI}
        </ul>
    <body/>
    </html>
    ''')
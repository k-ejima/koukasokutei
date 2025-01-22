from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView,DetailView
from .models import AddNews,Comment

from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage

from .forms import SearchForm


class IndexView(ListView):
    template_name = 'index.html'

    context_object_name = 'orderby_records'

    queryset = AddNews.objects.order_by('-posted_at')

    paginate_by = 5

class NewsDetail(DetailView):
    template_name = 'post.html'

    model = AddNews

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(news=self.object).order_by('-posted_at')
        context['form'] = CommentForm()
        return context

class GovernmentView(ListView):
    template_name = 'government_list.html'

    model = AddNews

    context_object_name = 'government_records'

    queryset = AddNews.objects.filter(category='government').order_by('-posted_at')

    paginate_by = 2

class EntertainmentView(ListView):
    template_name = 'entertainment_list.html'

    model = AddNews

    context_object_name = 'entertainment_records'

    queryset = AddNews.objects.filter(category='entertainment').order_by('-posted_at')

    paginate_by = 2

class SportsView(ListView):
    template_name = 'sports_list.html'

    model = AddNews

    context_object_name = 'sports_records'

    queryset = AddNews.objects.filter(category='sports').order_by('-posted_at')

    paginate_by = 2


class ContactView(FormView):

    template_name = 'contact.html'

    form_class = ContactForm

    success_url = reverse_lazy('Ejinews:contact')

    def form_valid(self, form):

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject = 'お問い合わせ: {}'.format(title)

        message = '送信者名: {0}\nメールアドレス: {1}\n タイトル:{2}\n メッセージ:{3}'.format(name,email,title,messages)
        
        from_email = 'fko2447004@stu.o-hara.ac.jp'

        to_list = ['fko2447004@stu.o-hara.ac.jp']

        message = EmailMessage(subject=subject,
                            body=message,from_email=from_email,
                            to=to_list,
                            )
        
        message.send()

        messages.success(
            self.request, 'お問い合わせは正常に送信されました。')
        
        return super().form_valid(form)



# search: 検索機能を処理し、クエリに基づいてニュース記事をフィルタリングし、結果を表示
def search(request):
    # SearchFormのインスタンスを作成
    form = SearchForm()
    # 結果を格納するための空のリストを初期化
    results = []
    # リクエストのGETパラメータに'query'が含まれているか確認
    if 'query' in request.GET:
        # GETパラメータを使用してSearchFormのインスタンスを作成
        form = SearchForm(request.GET)
        # フォームが有効かどうかを検証
        if form.is_valid():
            # フォームからクエリを取得
            query = form.cleaned_data['query']
            # タイトルまたはコンテンツにクエリが含まれているニュース記事をフィルタリング
            results = AddNews.objects.filter(title__icontains=query) | AddNews.objects.filter(content__icontains=query)
    # search_results.htmlテンプレートをレンダリングし、フォームと結果をコンテキストとして渡す
    return render(request, 'search_results.html', {'form': form, 'results': results})


@login_required
def add_comment(request, news_id):
    # 指定されたIDのニュース記事を取得。存在しない場合は404エラーを返す。
    news = get_object_or_404(AddNews, id=news_id)
    
    # リクエストがPOSTメソッドの場合、フォームデータを処理する。
    if request.method == 'POST':
        # POSTデータを使用してCommentFormのインスタンスを作成。
        form = CommentForm(request.POST)
        
        # フォームが有効かどうかを検証。
        if form.is_valid():
            # フォームからコメントオブジェクトを作成するが、まだデータベースには保存しない。
            comment = form.save(commit=False)
            # コメントに関連するニュース記事を設定。
            comment.news = news
            # コメントに関連するユーザーを設定。
            comment.user = request.user
            # コメントをデータベースに保存。
            comment.save()
            # コメントが正常に保存された後、ニュース詳細ページにリダイレクト。
            return redirect('Ejinews:news_detail', pk=news.id)
    else:
        # リクエストがPOSTメソッドでない場合、空のフォームを作成。
        form = CommentForm()
    
    # フォームとニュース記事をコンテキストとしてテンプレートに渡す。
    return render(request, 'post.html', {'form': form, 'object': news})
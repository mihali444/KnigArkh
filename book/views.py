from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, UpdateView, CreateView

from book.forms import BookForm
from book.models import Author, Publisher, Book
from category.models import Category
from main.forms import BookOfferForm
from main.models import BookOffer, Photo
from user.models import Favorite


# Create your views here.
@require_http_methods(['POST'])
def toggle_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Требуется вход в систему'},
            status=403
        )

    offer_id = request.POST.get('offer_id')
    try:
        offer = BookOffer.objects.get(id=offer_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, offer=offer)
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
        return JsonResponse({'status': 'success', 'is_favorite': is_favorite})
    except BookOffer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Книга не найдена'}, status=404)


class ShowBookAnnouncement(DetailView):
    template_name = 'book/advertisement.html'
    model = BookOffer
    context_object_name = 'offer'

    def get_object(self, **kwargs):
        return get_object_or_404(BookOffer, uuid_post=self.kwargs['uuid_post'], is_published=True)


@login_required
def create_book_offer(request):
    """View for creating a new book offer with book information"""
    if request.method == 'POST':
        # Process the book form
        book_form = BookForm(request.POST, request.FILES)

        print("Book form valid:", book_form.is_valid())
        if not book_form.is_valid():
            print("Book form errors:", book_form.errors)

        if book_form.is_valid():
            # Get author by ID
            author_id = request.POST.get('author')
            author = Author.objects.get(id=author_id)

            # Save the book without committing to DB yet
            book = book_form.save(commit=False)
            book.author = author
            book.save()

            # Save many-to-many relationships
            book_form.save_m2m()

            # Print request.POST for debugging
            print("POST data:", request.POST)
            print("FILES data:", request.FILES)

            # Initialize book_offer_form with the book object
            book_offer_form = BookOfferForm(request.POST, initial={'book': book})
            book_offer_form.instance.book = book

            print("Book offer form valid:", book_offer_form.is_valid())
            if not book_offer_form.is_valid():
                print("Book offer form errors:", book_offer_form.errors)

            if book_offer_form.is_valid():
                book_offer = book_offer_form.save(commit=False)
                book_offer.user = request.user
                book_offer.book = book
                book_offer.is_published = True
                book_offer.is_active = 'Active'
                book_offer.save()

                # Save photos to the BookOffer
                for image in request.FILES.getlist('img'):
                    # Create a Photo instance but don't save it yet
                    photo = Photo(book=book_offer)
                    # Save the image to the photo's image field
                    photo.image.save(image.name, image)
                    # Now save the photo instance
                    photo.save()

                # Redirect to the book offer page
                return redirect(reverse('book:book-offer', kwargs={'uuid_post': book_offer.uuid_post}))
            else:
                # If book_offer_form is not valid, create it anyway
                book_offer = BookOffer(
                    user=request.user,
                    book=book,
                    description=request.POST.get('description', ''),
                    edition_year=request.POST.get('edition_year', 2000),
                    address=request.POST.get('address', ''),
                    is_published=True,
                    is_active='Active'
                )
                book_offer.save()

                # Save photos to the BookOffer
                for image in request.FILES.getlist('img'):
                    # Create a Photo instance but don't save it yet
                    photo = Photo(book=book_offer)
                    # Save the image to the photo's image field
                    photo.image.save(image.name, image)
                    # Now save the photo instance
                    photo.save()

                # Redirect to the book offer page
                return redirect(reverse('book:book-offer', kwargs={'uuid_post': book_offer.uuid_post}))

        # If forms are not valid, render the page with errors
        # Get all categories, publishers, and authors from the database
        categories = Category.objects.all()
        publishers = Publisher.objects.all()
        authors = Author.objects.all()

        # Initialize book_offer_form if it's not already defined
        if 'book_offer_form' not in locals():
            book_offer_form = BookOfferForm(request.POST)

        return render(request, 'book/new-advertisement.html', {
            'book_form': book_form,
            'book_offer_form': book_offer_form,
            'categories': categories,
            'publishers': publishers,
            'authors': authors,
        })

    # For GET requests, show empty forms
    # Get all categories, publishers, and authors from the database
    categories = Category.objects.all()
    publishers = Publisher.objects.all()
    authors = Author.objects.all()

    return render(request, 'book/new-advertisement.html', {
        'book_form': BookForm(),
        'book_offer_form': BookOfferForm(),
        'categories': categories,
        'publishers': publishers,
        'authors': authors,
    })


class EditBookOffer(LoginRequiredMixin, UpdateView):
    """View for editing an existing book offer"""
    template_name = 'book/new-advertisement.html'
    model = BookOffer
    form_class = BookOfferForm
    context_object_name = 'book_offer'

    def dispatch(self, request, *args, **kwargs):
        """Check if the user is the owner of the book offer before proceeding"""
        try:
            book_offer = BookOffer.objects.get(uuid_post=self.kwargs['uuid_post'])
            if book_offer.user != request.user:
                # User is not the owner, redirect with error message
                from django.contrib import messages
                messages.error(request, 'Вы можете редактировать только свои объявления.')
                return redirect('book:book-offer', uuid_post=self.kwargs['uuid_post'])
            return super().dispatch(request, *args, **kwargs)
        except BookOffer.DoesNotExist:
            # Book offer not found, return 404
            return get_object_or_404(BookOffer, uuid_post=self.kwargs['uuid_post'])

    def get_object(self, queryset=None):
        """Get the BookOffer object by uuid_post"""
        return get_object_or_404(BookOffer, uuid_post=self.kwargs['uuid_post'], user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add BookForm and other context data"""
        context = super().get_context_data(**kwargs)
        book_offer = self.get_object()

        # If form was submitted but invalid, use POST data
        if self.request.method == 'POST':
            context['book_form'] = BookForm(self.request.POST, self.request.FILES, instance=book_offer.book)
            context['book_offer_form'] = BookOfferForm(self.request.POST, instance=book_offer)
        else:
            # For GET requests, initialize forms with existing data
            context['book_form'] = BookForm(instance=book_offer.book)
            context['book_offer_form'] = BookOfferForm(instance=book_offer)

        # Add categories, publishers, and authors to context
        context['categories'] = Category.objects.all()
        context['publishers'] = Publisher.objects.all()
        context['authors'] = Author.objects.all()

        return context

    def form_valid(self, form):
        """Process the form data when valid"""
        book_form = BookForm(self.request.POST, self.request.FILES, instance=self.get_object().book)

        if book_form.is_valid():
            # Get author by ID
            author_id = self.request.POST.get('author')
            if author_id:
                author = Author.objects.get(id=author_id)
                # Save the book without committing to DB yet
                book = book_form.save(commit=False)
                book.author = author
                book.save()
                # Save many-to-many relationships
                book_form.save_m2m()
            else:
                # If no author selected, just save the book form
                book = book_form.save()

            # Save the book offer
            book_offer = form.save(commit=False)
            book_offer.book = book
            book_offer.save()

            # Handle photos if new ones are uploaded
            if self.request.FILES.getlist('img'):
                # Delete existing photos
                Photo.objects.filter(book=book_offer).delete()

                # Save new photos
                for image in self.request.FILES.getlist('img'):
                    photo = Photo(book=book_offer)
                    photo.image.save(image.name, image)
                    photo.save()

            return redirect(reverse('book:book-offer', kwargs={'uuid_post': book_offer.uuid_post}))
        else:
            # If book_form is not valid, re-render the form with errors
            return self.form_invalid(form)

    def get_success_url(self):
        """Return URL to redirect to after successful edit"""
        return reverse_lazy('book:book-offer', kwargs={'uuid_post': self.get_object().uuid_post})

from typing import Any, Dict, List, Optional
from django.db import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse

from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    UpdateView,
    DeleteView,
    CreateView,
    View,
)
import json

from .models import Message, Room, Thread, DiscussionRoom
from .forms import DiscussionRoomForm, BulkMessageForm, InviteForm


class RoomDetailView(DetailView):
    context_object_name = "room"
    queryset = Room.objects.all()
    template_name = "chats/room.html"


class DiscussionDetailView(DetailView):
    context_object_name = "room"
    queryset = DiscussionRoom.objects.all()
    template_name = "chats/discussion_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        obj = self.get_object()
        ctx = super().get_context_data(**kwargs)
        ctx["room_name_json"] = mark_safe(json.dumps(obj.room.id))
        ctx["username"] = mark_safe(json.dumps(self.request.user.username))

        return ctx


# @login_required
# def discussion_room(request, slug):
#     # room_obj, new_obj = Room.objects.new_or_get(request)
#     room = get_object_or_404(DiscussionRoom, slug=slug)
#     room_name = room.room.id
#     return render(
#         request,
#         "chats/discussion_room.html",
#         {
#             "room": room,
#             "room_name_json": mark_safe(json.dumps(room_name)),
#             "username": mark_safe(json.dumps(request.user.username)),
#         },
#     )


class DiscussionListView(ListView):
    context_object_name = "rooms"
    paginate_by = 16

    def get_queryset(self) -> QuerySet[Any]:
        queryset = DiscussionRoom.objects.all()
        sort = self.request.GET.get("sort")
        if sort == "newest":
            queryset = queryset.order_by("-created")
        elif sort == "oldest":
            queryset = queryset.order_by("created")
        else:
            sort = "trendings"
            queryset = DiscussionRoom.objects.get_trendings(qs=queryset)

        return queryset

    def get_template_names(self) -> List[str]:
        if self.request.htmx:
            return "chats/partials/discussions.html"
        return "chats/discussions.html"

    def get_paginate_by(self, queryset: QuerySet[Any]) -> int | None:
        paginate_by = self.request.GET.get("paginate_by")
        if paginate_by:
            return paginate_by
        return super().get_paginate_by(queryset)


# def discussion_list(request):
#     discussions = DiscussionRoom.objects.all()
#     sort = request.GET.get("sort")
#     if sort == "newest":
#         discussions = discussions.order_by("-created")
#     elif sort == "oldest":
#         discussions = discussions.order_by("created")
#     else:
#         sort = "trendings"
#         discussions = DiscussionRoom.objects.get_trendings(qs=discussions)

#     paginator = Paginator(discussions, 2)  # Show 16 discussion per page.

#     page_number = request.GET.get("page")
#     if page_number is None:
#         page_number = 1
#     page_obj = paginator.get_page(page_number)

#     context = {
#         "page_number": page_number,
#         "rooms": page_obj,
#         "page_number": int(page_number),
#         "num_pages": paginator.num_pages,
#         "sort": sort,
#     }
#     if request.htmx:
#         return render(request, "chats/partials/discussion_card.html", context)
#     return render(request, "chats/discussions.html", context)


class UserRoomListView(ListView):
    context_object_name = "rooms"
    paginate_by = 1

    def get_queryset(self) -> QuerySet[Any]:
        queryset = DiscussionRoom.objects.filter(members=self.request.user).order_by(
            "room__updated"
        )
        return queryset

    def get_template_names(self) -> List[str]:
        if self.request.GET.get("display") == "modal" and self.request.GET.get(
            "paginat"
        ):
            return "chats/partials/user_rooms_popup_body.html"
        if self.request.GET.get("display") == "modal":
            return "chats/partials/user_rooms_popup.html"
        return "chats/partials/user_rooms.html"


# @login_required
# def user_rooms(request):
#     discussions = DiscussionRoom.objects.filter(members=request.user).order_by(
#         "room__updated"
#     )
#     user_rooms_count = discussions.count()
#     paginator = Paginator(discussions, 3)  # Show 3 rooms per page.

#     page_number = request.GET.get("page")
#     if page_number is None:
#         page_number = 1

#     rooms = paginator.get_page(page_number)

#     context = {
#         "rooms": rooms,
#         "user_rooms_count": user_rooms_count,
#         "page_number": int(page_number),
#         "num_pages": paginator.num_pages,
#     }
#     if request.GET.get("display") == "sticky":
#         template_name = "chats/partials/user_rooms.html"
#     else:
#         template_name = "chats/partials/user_rooms_popup.html"
#     return render(request, template_name, context)


class Trendings(ListView):
    queryset = DiscussionRoom.objects.get_trendings()
    template_name = "chats/trendings.html"
    context_object_name = "discussions"
    paginate_by = 3


# @login_required
# def trendings(request):
#     discussions = DiscussionRoom.objects.get_trendings()
#     return render(request, "chats/trendings.html", {"discussions": discussions})


class InvitePeople(FormView):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = InviteForm(request.POST)
        # print(form.cleaned_data("users"))
        print(form.data.get("users"))
        users_pks = [int(pk) for pk in request.POST.getlist("users")]
        room_id = request.POST.get("room")
        d_room = get_object_or_404(DiscussionRoom, id=room_id)
        invitations = []
        User = get_user_model()
        usernames = [u.username for u in User.objects.filter(id__in=users_pks)]
        # for pk in users_pks:
        # 	invitations.append(CustomNotification(
        # 		type="invitation",
        # 		recipient=get_user_model().objects.get(id=pk),
        # 		actor=request.user,
        # 		verb=f'{request.user.get_name} sent you an invitation to join the discussion "{d_room.headline}"',
        # 		redirect_url=d_room.get_absolute_url
        # 	))
        # CustomNotification.objects.bulk_create(invitations)
        return HttpResponse(
            f"""
            <h5 class="text-success text-center">Invitation sent!</h5> 
            <p class="text-center">Your invitation has been sent to {[u for u in usernames]}</p>
            """
        )
        # return super().post(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = InviteForm(initial={"room": request.GET.get("room")})
        return render(request, "chats/invite.html", {"form": form})
        # return super().get(request, *args, **kwargs)


# @login_required
# def invite_people(request):
#     if request.method == "POST":
#         form = InviteForm(request.POST)
#         users_pks = request.POST.getlist("users")
#         room_id = request.POST.get("room")
#         d_room = get_object_or_404(DiscussionRoom, id=room_id)
#         invitations = []
#         # for pk in users_pks:
#         # 	invitations.append(CustomNotification(
#         # 		type="invitation",
#         # 		recipient=get_user_model().objects.get(id=pk),
#         # 		actor=request.user,
#         # 		verb=f'{request.user.get_name} sent you an invitation to join the discussion "{d_room.headline}"',
#         # 		redirect_url=d_room.get_absolute_url
#         # 	))
#         # CustomNotification.objects.bulk_create(invitations)
#         return HttpResponse(
#             """<h5 class="text-success text-center">Invitation sent!</h5>"""
#         )
#     else:
#         form = InviteForm(initial={"room": request.GET.get("room")})
#     return render(request, "chats/invite.html", {"form": form})


class DiscussionFormView(FormView):
    form_class = DiscussionRoomForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: Any) -> HttpResponse:
        d_room = form.save(commit=False)
        d_room.owner = self.request.user
        room_obj = Room.objects.create()
        d_room.room = room_obj
        d_room.save()
        d_room.members.add(d_room.owner)
        tags = form.cleaned_data.get("tags")
        d_room.tags.set(tags)
        return redirect(d_room.get_absolute_url)
        # return super().form_valid(form)

    def get_template_names(self) -> List[str]:
        if self.request.htmx:
            return "chats/partials/discussion_room_form.html"
        return "chats/discussion_room_form.html"


# @login_required
# def discussion_create(request):
#     form = DiscussionRoomForm(request.POST or None)
#     if form.is_valid():
#         d_room = form.save(commit=False)
#         d_room.owner = request.user
#         room_obj = Room.objects.create()
#         d_room.room = room_obj
#         d_room.save()
#         d_room.members.add(d_room.owner)
#         tags = form.cleaned_data.get("tags")
#         d_room.tags.set(tags)
#         return redirect(d_room.get_absolute_url)
#     if request.htmx:
#         template_name = "chats/partials/discussion_room_form.html"
#     else:
#         template_name = "chats/discussion_room_form.html"
#     return render(request, template_name, {"form": form})


class DiscussionUpdateView(UpdateView):
    form_class = DiscussionRoomForm
    queryset = DiscussionRoom.objects.all()
    # lookup_expr = 'pk'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        d_room = form.save()
        tags = form.cleaned_data.get("tags")
        d_room.tags.set(tags)
        return redirect(d_room.get_absolute_url)

    def get_template_names(self) -> List[str]:
        if self.request.htmx:
            return "chats/partials/discussion_room_form.html"
        return "chats/discussion_room_form.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["update"] = True
        return ctx


# @login_required
# def discussion_update(request, id):
#     room = get_object_or_404(DiscussionRoom, id=id)
#     form = DiscussionRoomForm(request.POST or None, instance=room)
#     if form.is_valid():
#         d_room = form.save()
#         tags = form.cleaned_data.get("tags")
#         d_room.tags.set(tags)
#         return redirect(d_room.get_absolute_url)
#     if request.htmx:
#         template_name = "chats/partials/discussion_room_form.html"
#     else:
#         template_name = "chats/discussion_room_form.html"
#     return render(
#         request,
#         template_name,
#         {
#             "form": form,
#             "update": True,
#         },
#     )


class DiscussionSearchView(ListView):
    template_name = "chats/search_room.html"
    context_object_name = "rooms"

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get("q")
        return DiscussionRoom.objects.search(query)


# def search_room(request):
#     query = request.GET.get("q")
#     search_result = DiscussionRoom.objects.search(query)
#     return render(
#         request,
#         "chats/search_room.html",
#         {"search_result": search_result, "query": query},
#     )


class ThreadListView(ListView):
    context_object_name = "rooms"

    def get_queryset(self) -> QuerySet[Any]:
        return Thread.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        ).distinct()

    def get_template_names(self) -> List[str]:
        if self.request.htmx:
            return "chats/partials/threads_nav.html"
        return "chats/threads.html"


# def threads(request):
#     rooms = Thread.objects.filter(
#         Q(user1=request.user) | Q(user2=request.user)
#     ).distinct()
#     template_name = "chats/threads.html"
#     if request.htmx:
#         template_name = "chats/partials/threads_nav.html"
#     return render(
#         request,
#         template_name,
#         {
#             "rooms": rooms,
#         },
#     )


class ThreadDetailView(DetailView):
    context_object_name = "thread"

    # def get_queryset(self) -> QuerySet[Any]:
    #     thread, created = Thread.objects.new_or_get(
    #         self.request.user, self.get_context_data["partner"]
    #     )
    #     return thread

    def get_object(self, queryset: QuerySet[Any] | None = ...):
        partner = get_object_or_404(get_user_model(), id=self.request.GET.get("pid"))
        thread, created = Thread.objects.new_or_get(self.request.user, partner)
        return thread

    def get_template_names(self) -> List[str]:
        if self.request.htmx and self.request.GET.get("display") == "popup":
            template_name = "chats/partials/thread_popup.html"
        elif self.request.htmx:
            template_name = "chats/partials/thread.html"
        else:
            template_name = "chats/thread_single.html"
        return template_name

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        thread = self.get_object()
        user = self.request.user
        ctx["partner"] = get_object_or_404(
            get_user_model(), id=self.request.GET.get("pid")
        )
        ctx["room"] = thread.room
        ctx["rooms"] = Thread.objects.filter(Q(user1=user) | Q(user2=user)).distinct()
        ctx["room_name_json"] = mark_safe(json.dumps(thread.room.id))
        ctx["username"] = mark_safe(json.dumps(user.username))

        return ctx


# @login_required
# def thread(request, partner_id):
#     partner = get_object_or_404(get_user_model(), id=partner_id)
#     thread, created = Thread.objects.new_or_get(request.user, partner)

#     display = request.GET.get("display")
#     if request.htmx and display == "popup":
#         template_name = "chats/partials/thread_popup.html"
#     elif request.htmx:
#         template_name = "chats/partials/thread.html"
#     else:
#         template_name = "chats/thread_single.html"

#     return render(
#         request,
#         template_name,
#         {
#             "partner": partner,
#             "thread": thread,
#             "room": thread.room,
#             "rooms": Thread.objects.filter(
#                 Q(user1=request.user) | Q(user2=request.user)
#             ).distinct(),
#             # "supports": PageSupport.objects.filter(members=request.user),
#             "room_name_json": mark_safe(json.dumps(thread.room.id)),
#             "username": mark_safe(json.dumps(request.user.username)),
#         },
#     )


class ThreadCreateView(FormView):
    form_class = BulkMessageForm
    template_name = "chats/thread_new.html"

    def form_valid(self, form):
        msg = form.cleaned_data.get("message")
        recipients = form.cleaned_data.get("recipients")
        msgs = []
        for user in recipients:
            thread, created = Thread.objects.new_or_get(self.request.user, user)
            message = Message.objects.create(
                author=self.request.user, room=thread.room, content=msg
            )
            msgs.append(message.id)
        names = [
            f'<span class="badge bg-dark me-1">{r.username}</span>' for r in recipients
        ]

        if self.request.htmx:
            return JsonResponse({"SUCCESS": "Message sent to", "messages": msgs})
        messages.success(self.request, f'Message sent to: {" ".join(names)}')
        return redirect("chats:threads")


# def thread_new(request):
#     if request.method == "POST":
#         form = BulkMessageForm(request.POST)
#         if form.is_valid():
#             msg = form.cleaned_data.get("message")
#             recipients = form.cleaned_data.get("recipients")
#             msgs = []
#             for user in recipients:
#                 thread, created = Thread.objects.new_or_get(request.user, user)
#                 message = Message.objects.create(
#                     author=request.user, room=thread.room, content=msg
#                 )
#                 msgs.append(message.id)
#             names = [
#                 f'<span class="badge bg-dark me-1">{r.username}</span>'
#                 for r in recipients
#             ]

#             if request.htmx:
#                 return JsonResponse({"SUCCESS": "Message sent to", "messages": msgs})
#             messages.success(request, f'Message sent to: {" ".join(names)}')
#             return redirect("chats:threads")
#     else:
#         form = BulkMessageForm()
#     return render(request, "chats/thread_new.html", {"form": form})


class ClearHistory(View):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        room_id = request.POST.get("room_id")
        room = get_object_or_404(Room, id=room_id)
        deleted_msg_count = room.clear_chat_history()
        msg = f"{deleted_msg_count} messages has been deleted."
        if request.htmx:
            return JsonResponse(
                {"deleted_msg_count": deleted_msg_count, "message": msg}
            )
        else:
            messages.success(request, msg)
            partner_id = request.POST.get("partner_id")
            if partner_id:
                return redirect(
                    reverse("chats:thread", kwargs={"pk": room_id})
                    + f"?pid={partner_id}"
                )

            discussion_slug = request.POST.get("discussion_slug")
            if discussion_slug:
                return redirect("chats:discussion_room", discussion_slug)
            return redirect(request.path)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        room_id = request.GET.get("room_id")
        partner_id = request.GET.get("partner_id")
        return render(
            request,
            "chats/partials/clear_history_popup.html",
            {"room_id": room_id, "partner_id": partner_id},
        )


# def chat_clear_history(request):
#     if request.method == "POST":
#         room_id = request.POST.get("room_id")
#         room = get_object_or_404(Room, id=room_id)
#         deleted_msg_count = room.clear_chat_history()
#         msg = f"{deleted_msg_count} messages has been deleted."
#         if request.htmx:
#             return JsonResponse(
#                 {"deleted_msg_count": deleted_msg_count, "message": msg}
#             )
#         else:
#             messages.success(request, msg)
#             partner_id = request.POST.get("partner_id")
#             if partner_id:
#                 return redirect("chats:thread", partner_id)

#             discussion_slug = request.POST.get("discussion_slug")
#             if discussion_slug:
#                 return redirect("chats:discussion_room", discussion_slug)
#             return redirect(request.path)
#     else:
#         room_id = request.GET.get("room_id")
#         partner_id = request.GET.get("partner_id")
#         return render(
#             request,
#             "chats/partials/clear_history_popup.html",
#             {"room_id": room_id, "partner_id": partner_id},
#         )


class RoomDeleteView(DeleteView):
    context_object_name = "room"
    queryset = Room.objects.all()
    template_name = "chats/partials/chat_delete_popup.html"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.get_object().delete()
        msg = "Chat has been deleted."
        if request.htmx:
            return JsonResponse({"deleted": True, "message": msg})
        else:
            messages.success(request, msg)
            next = request.POST.get("next")
            if next:
                return redirect(next)
        return redirect("chats:threads")


# def chat_delete(request):
#     room_id = request.GET.get("room_id")
#     if request.method == "POST":
#         get_object_or_404(Room, id=room_id).delete()
#         msg = "Chat has been deleted."
#         if request.htmx:
#             return JsonResponse({"deleted": True, "message": msg})
#         else:
#             messages.success(request, msg)
#             next = request.POST.get("next")
#             if next:
#                 return redirect(next)
#             return redirect("chats:threads")
#     else:
#         return render(
#             request, "chats/partials/chat_delete_popup.html", {"room_id": room_id}
#         )


class RoomMutate(View):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        room_id = request.POST.get("room_id")
        room = get_object_or_404(Room, id=room_id)
        room.muted = not room.muted
        room.save()
        msg = "Chat has been muted." if room.muted else "Chat has been unmuted."
        if request.htmx or request.is_ajax():
            return JsonResponse({"muted": room.muted, "msg": msg})
        else:
            messages.success(request, msg)
            next = request.POST.get("next")
            if next:
                return redirect(next)
            return redirect("chats:threads")


# def chat_mute(request):
#     if request.method == "POST":
#         room_id = request.POST.get("room_id")
#         room = get_object_or_404(Room, id=room_id)
#         room.muted = not room.muted
#         room.save()
#         msg = "Chat has been muted." if room.muted else "Chat has been unmuted."
#         if request.htmx or request.is_ajax():
#             return JsonResponse({"muted": room.muted, "msg": msg})
#         else:
#             messages.success(request, msg)
#             next = request.POST.get("next")
#             if next:
#                 return redirect(next)
#             return redirect("chats:threads")


def total_unread_messages(request):
    unread_msgs = Thread.objects.total_unread_messages(request.user)
    return JsonResponse({"total_unread_counter": unread_msgs})

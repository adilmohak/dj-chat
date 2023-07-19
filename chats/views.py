from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

# from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
import json

# from notifications.models import CustomNotification
from .models import Message, PageSupport, Room, Thread, DiscussionRoom
from .forms import DiscussionRoomForm, BulkMessageForm, InviteForm


def index(request):
    return render(request, "chats/index.html", {})


# @login_required
# def room(request, id):
# 	# room_obj, new_obj = Room.objects.new_or_get(request)
# 	room = get_object_or_404(DiscussionRoom, id=id)
# 	room_name = room.room.id
# 	return render(request, 'chats/room.html', {
# 		'room': room,
# 		'room_name_json': mark_safe(json.dumps(room_name)),
# 		'username': mark_safe(json.dumps(request.user.username))
# 	})


@login_required
def discussion_room(request, slug):
    # room_obj, new_obj = Room.objects.new_or_get(request)
    room = get_object_or_404(DiscussionRoom, slug=slug)
    room_name = room.room.id
    return render(
        request,
        "chats/discussion_room.html",
        {
            "room": room,
            "room_name_json": mark_safe(json.dumps(room_name)),
            "username": mark_safe(json.dumps(request.user.username)),
        },
    )


@login_required
def recent_rooms(request):
    discussions = DiscussionRoom.objects.filter(members=request.user).order_by(
        "room__updated"
    )
    recent_rooms_count = discussions.count()
    paginator = Paginator(discussions, 3)  # Show 3 rooms per page.

    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1

    rooms = paginator.get_page(page_number)

    context = {
        "page_number": page_number,
        "rooms": rooms,
        "recent_rooms_count": recent_rooms_count,
        "page_number": int(page_number),
        "num_pages": paginator.num_pages,
    }
    if request.GET.get("display") == "sticky":
        template_name = "chats/partials/recent_rooms.html"
    else:
        template_name = "chats/partials/recent_rooms_popup.html"
    return render(request, template_name, context)


def discussion_list(request):
    discussions = DiscussionRoom.objects.all()
    sort = request.GET.get("sort")
    if sort == "newest":
        discussions = discussions.order_by("-created")
    elif sort == "oldest":
        discussions = discussions.order_by("created")
    else:
        sort = "trendings"
        discussions = DiscussionRoom.objects.get_trendings(qs=discussions)

    paginator = Paginator(discussions, 16)  # Show 16 discussion per page.

    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    context = {
        "page_number": page_number,
        "rooms": page_obj,
        "page_number": int(page_number),
        "num_pages": paginator.num_pages,
        "sort": sort,
    }
    if request.htmx:
        return render(request, "chats/partials/discussion_card.html", context)
    return render(request, "chats/discussions.html", context)


@login_required
def trendings(request):
    discussions = DiscussionRoom.objects.get_trendings()
    return render(request, "chats/trendings.html", {"discussions": discussions})


@login_required
def invite_people(request):
    if request.method == "POST":
        form = InviteForm(request.POST)
        users_pks = request.POST.getlist("users")
        room_id = request.POST.get("room")
        d_room = get_object_or_404(DiscussionRoom, id=room_id)
        invitations = []
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
            """<h5 class="text-success text-center">Invitation sent!</h5>"""
        )
    else:
        form = InviteForm(initial={"room": request.GET.get("room")})
    return render(request, "chats/invite.html", {"form": form})


@login_required
def discussion_create(request):
    form = DiscussionRoomForm(request.POST or None)
    if form.is_valid():
        d_room = form.save(commit=False)
        d_room.owner = request.user
        room_obj = Room.objects.create()
        d_room.room = room_obj
        d_room.save()
        d_room.members.add(d_room.owner)
        tags = form.cleaned_data.get("tags")
        d_room.tags.set(tags)
        return redirect(d_room.get_absolute_url)
    if request.htmx:
        template_name = "chats/partials/discussion_room_form.html"
    else:
        template_name = "chats/discussion_room_form.html"
    return render(request, template_name, {"form": form})


@login_required
def discussion_update(request, id):
    room = get_object_or_404(DiscussionRoom, id=id)
    form = DiscussionRoomForm(request.POST or None, instance=room)
    if form.is_valid():
        d_room = form.save()
        tags = form.cleaned_data.get("tags")
        d_room.tags.set(tags)
        return redirect(d_room.get_absolute_url)
    if request.htmx:
        template_name = "chats/partials/discussion_room_form.html"
    else:
        template_name = "chats/discussion_room_form.html"
    return render(
        request,
        template_name,
        {
            "form": form,
            "update": True,
        },
    )


def search_room(request):
    query = request.GET.get("q")
    search_result = DiscussionRoom.objects.search(query)
    return render(
        request,
        "chats/search_room.html",
        {"search_result": search_result, "query": query},
    )


def threads(request):
    rooms = Thread.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).distinct()
    template_name = "chats/threads.html"
    if request.htmx:
        template_name = "chats/partials/threads_nav.html"
    return render(
        request,
        template_name,
        {
            "rooms": rooms,
        },
    )


@login_required
def thread(request, partner_id):
    partner = get_object_or_404(get_user_model(), id=partner_id)
    thread, created = Thread.objects.new_or_get(request.user, partner)

    display = request.GET.get("display")
    if request.htmx and display == "popup":
        template_name = "chats/partials/thread_popup.html"
    elif request.htmx:
        template_name = "chats/partials/thread.html"
    else:
        template_name = "chats/thread_single.html"

    return render(
        request,
        template_name,
        {
            "partner": partner,
            "thread": thread,
            "room": thread.room,
            "rooms": Thread.objects.filter(
                Q(user1=request.user) | Q(user2=request.user)
            ).distinct(),
            "supports": PageSupport.objects.filter(members=request.user),
            "room_name_json": mark_safe(json.dumps(thread.room.id)),
            "username": mark_safe(json.dumps(request.user.username)),
        },
    )


@login_required
def page_support(request, page_id):
    # user = get_object_or_404(User, i)
    # page = get_object_or_404(Collection, id=page_id)
    # support_group, created = PageSupport.objects.new_or_get(request.user, page)

    display = request.GET.get("display")
    if request.htmx and display == "popup":
        template_name = "chats/partials/page_support_popup.html"
    elif request.htmx:
        template_name = "chats/partials/page_support.html"
    else:
        template_name = "chats/page_support_single.html"

    return render(
        request,
        template_name,
        {
            "partner": request.user,
            # 'support_group': support_group,
            # 'page': page,
            # 'room': support_group.room,
            # 'rooms': Thread.objects.filter(Q(user1=request.user) | Q(user2=request.user)).distinct(),
            # 'room_name_json': mark_safe(json.dumps(support_group.room.id)),
            "username": mark_safe(json.dumps(request.user.username)),
        },
    )


def thread_new(request):
    if request.method == "POST":
        form = BulkMessageForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data.get("message")
            recipients = form.cleaned_data.get("recipients")
            msgs = []
            for user in recipients:
                thread, created = Thread.objects.new_or_get(request.user, user)
                message = Message.objects.create(
                    author=request.user, room=thread.room, content=msg
                )
                msgs.append(message.id)
            names = [
                f'<span class="badge bg-dark me-1">{r.username}</span>'
                for r in recipients
            ]

            if request.htmx:
                return JsonResponse({"SUCCESS": "Message sent to", "messages": msgs})
            messages.success(request, f'Message sent to: {" ".join(names)}')
            return redirect("chats:threads")
    else:
        form = BulkMessageForm()
    return render(request, "chats/thread_new.html", {"form": form})


def chat_clear_history(request):
    if request.method == "POST":
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
                return redirect("chats:thread", partner_id)

            discussion_slug = request.POST.get("discussion_slug")
            if discussion_slug:
                return redirect("chats:discussion_room", discussion_slug)
            return redirect(request.path)
    else:
        room_id = request.GET.get("room_id")
        partner_id = request.GET.get("partner_id")
        return render(
            request,
            "chats/partials/clear_history_popup.html",
            {"room_id": room_id, "partner_id": partner_id},
        )


def chat_delete(request):
    room_id = request.GET.get("room_id")
    if request.method == "POST":
        get_object_or_404(Room, id=room_id).delete()
        msg = "Chat has been deleted."
        if request.htmx:
            return JsonResponse({"deleted": True, "message": msg})
        else:
            messages.success(request, msg)
            next = request.POST.get("next")
            if next:
                return redirect(next)
            return redirect("chats:threads")
    else:
        return render(
            request, "chats/partials/chat_delete_popup.html", {"room_id": room_id}
        )


def chat_mute(request):
    if request.method == "POST":
        room_id = request.POST.get("room_id")
        room = get_object_or_404(Room, id=room_id)
        room.muted = not room.muted
        room.save()
        msg = "Chat has been muted." if room.muted else "Chat has been unmuted."
        if request.htmx:
            return JsonResponse({"muted": room.muted, "msg": msg})
        else:
            messages.success(request, msg)
            next = request.POST.get("next")
            if next:
                return redirect(next)
            return redirect("chats:threads")


def total_unread_messages(request):
    unread_msgs = Thread.objects.total_unread_messages(request.user)
    return JsonResponse({"total_unread_counter": unread_msgs})

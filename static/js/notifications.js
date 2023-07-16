window.addEventListener('DOMContentLoaded', () => {
    
    // --------------------------
    // Constants
    // --------------------------
    // const $notifyCounterEl = $('#total-unread-notifications');
    const $mainNotifyCounterEl = $('#total-unread-main-notifications-counter');
    const $discussionCounterEl = $('#total-unread-discussion-notifications-counter');
    const $unreadMsgsEl        = $('#total-unread-msgs');
    const $cartItemsCounterEl  = $('#cart-items-counter');

    // --------------------------
    // End constants
    // --------------------------

    let CustomNotificationSocket = new ReconnectingWebSocket(
		(window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
		+ window.location.host
		+ '/ws/custom-notification/'
    );
    
    function fetchNotifications() {
        CustomNotificationSocket.send(JSON.stringify({'command': 'fetch_discussion_notifications'}));
    }

    function fetchCounter() {
        CustomNotificationSocket.send(JSON.stringify({'command': 'fetch_counter'}));
    }
    
    function _createDiscussionNotification(notification) {
        let n_item = `<li>
                        <a class="dropdown-item d-flex align-items-center px-2 unread"
                            href="${notification.redirect_url}">
                            <img src="${notification.icon}" width="45px" class="me-2 undraggable" alt="">
                            <div>
                                <p class="small triple-line-truncate">
                                    ${notification.actor.name} 
                                    ${notification.verb}
                                </p>
                            </div>
                        </a>
                    </li>`;
        $('#notifications-list').prepend(n_item);
    }
    function createChatNotification(notification) {
        let n_item = `<a class="dropdown-item d-flex align-items-center unread" href="${notification.redirect_url}">
            <div class="me-3 position-relative">
                <div class="avatar avatar-md">
                    <img src="${notification.icon}" alt="">
                </div>
                <div class="status-indicator bg-success"></div>
            </div>
            <div>
                <div class="text-truncate small">${notification.verb}</div>
                <div class="small text-gray-500">${notification.actor.name} · ${notification.created}</div>
            </div>
        </a>`;
        $('#chat-notifications-list').prepend(n_item);
    }
    function createMainNotification(notification) {
        let n_item = `<li>
                        <a class="dropdown-item d-flex align-items-center px-2 unread"
                            href="${notification.redirect_url}">
                            <img src="${notification.icon}" width="45px" class="me-2 undraggable" alt="">
                            <div>
                                <p class="small triple-line-truncate">
                                    ${notification.actor.name} 
                                    ${notification.verb}
                                </p>
                            </div>
                        </a>
                    </li>`;
        $('#main-notifications-list').prepend(n_item);
    }
    
    CustomNotificationSocket.onopen = function (e) {
        fetchCounter();
    };
    
    CustomNotificationSocket.onmessage = function (event) {
        let data = JSON.parse(event.data);
        console.log("data", data)
        if (data['command'] === 'notifications') {
            let discussion_notifications = JSON.parse(data['discussion_notifications']);
            let chat_notifications = JSON.parse(data['chat_notifications']);
            let other_notifications = JSON.parse(data['other_notifications']);
            attachDiscussion(discussion_notifications)
            attachChat(chat_notifications)
            attachOther(other_notifications)
        } 
        else if (data['command'] === 'new_discussion_notification') {
            // let notification = $('#total-unread-notifications');
            // notification.text(parseInt(notification.text()) + 1);
            _createDiscussionNotification(JSON.parse(data['notification']));
        }
        else if (data['command'] === 'notifications_count') {
            if (!(data['discussion_notify_count'] === 0)) {
                $discussionCounterEl.parent('.notify-badge').css('display', 'block')
                $discussionCounterEl.text(data['discussion_notify_count']);
            }
            if (!(data['chat_notify_count'] === 0)) {
                $discussionCounterEl.parent('.notify-badge').css('display', 'block')
                $discussionCounterEl.text(data['chat_notify_count']);
            }
            if (!(data['other_notify_count'] === 0)) {
                $mainNotifyCounterEl.parent('.notify-badge').css('display', 'block')
                $mainNotifyCounterEl.text(data['other_notify_count']);
            }
        }
    };

    function attachDiscussion(notification) {
        if(notification.length > 0){
            $discussionCounterEl.parent('.notify-badge').css('display', 'block')
            $discussionCounterEl.text(notification.length);
            for (let i = 0; i < notification.length; i++) {
                _createDiscussionNotification(notification[i]);
            }
        }
        else {$discussionCounterEl.parent('.notify-badge').css('display', 'none')}
    }
    function attachChat(notification) {
        if(notification.length > 0){
            $('#total-unread-chat-notifications-counter').parent('.notify-badge').css('display', 'block')
            $('#total-unread-chat-notifications-counter').text(notification.length);
            for (let i = 0; i < notification.length; i++) {
                createChatNotification(notification[i]);
            }
        }
        else {$('#total-unread-chat-notifications-counter').parent('.notify-badge').css('display', 'none')}
    }
    function attachOther(notification) {
        if(notification.length > 0){
            $('#total-unread-main-notifications-counter').parent('.notify-badge').css('display', 'block')
            $('#total-unread-main-notifications-counter').text(notification.length);
            for (let i = 0; i < notification.length; i++) {
                createMainNotification(notification[i]);
            }
        }
        else {$('#total-unread-main-notifications-counter').parent('.notify-badge').css('display', 'none')}
    }

    


    // function notifyCounter(notification) {
    //     if(notification.length > 0){
    //         $discussionCounterEl.parent('.notify-badge').css('display', 'block')
    //         $discussionCounterEl.text(notification.length);
    //         for (let i = 0; i < notification.length; i++) {
    //             _createDiscussionNotification(notification[i]);
    //         }
    //     }
    //     else {$discussionCounterEl.parent('.notify-badge').css('display', 'none')}
    // }
    // function chatCounter(notification) {
    //     if(notification.length > 0){
    //         $('#total-unread-chat-notifications-counter').parent('.notify-badge').css('display', 'block')
    //         $('#total-unread-chat-notifications-counter').text(notification.length);
    //         for (let i = 0; i < notification.length; i++) {
    //             createChatNotification(notification[i]);
    //         }
    //     }
    //     else {$('#total-unread-chat-notifications-counter').parent('.notify-badge').css('display', 'none')}
    // }
    function notifyCounter(notification) {
        if(notification.length > 0){
            $('#total-unread-main-notifications-counter').parent('.notify-badge').css('display', 'block')
            $('#total-unread-main-notifications-counter').text(notification.length);
            for (let i = 0; i < notification.length; i++) {
                createMainNotification(notification[i]);
            }
        }
        else {$('#total-unread-main-notifications-counter').parent('.notify-badge').css('display', 'none')}
    }
})

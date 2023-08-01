// import * from 'utils';
// var utils = require('./utils');

/*jslint browser:true */
"use strict";

(function ($) {
  $.fn.chat = function (
    roomName,
    username,
    roomId,
    msg_counter_url = null,
    group = false
  ) {
    console.log("roomName", roomName, "username", username, "roomId", roomId);
    // Chat socket closed/disconnected handler
    function websocketDisconnected() {
      toastr.warning("WebSocket disconnected. reconnecting...");
    }

    // Chat socket connected handler
    function websocketConnected() {
      toastr.success("WebSocket Connected.");
    }
    /*
     * ------------------------------------------------------------------------
     * variables
     * ------------------------------------------------------------------------
     */
    const msgInput = $("#chat-message-input");
    const chatSubmit = $("#chat-message-submit");
    const chatLog = $("#chat-log");
    const chatBody = $(".chat-body");
    const loadMoreBtn = $("#load-more");
    const emptyMessage =
      $.parseHTML(`<div class="empty-msg d-block mb-auto bg-light p-2">
						<h6 class="text-center small">Empty messages</h6>
						<p class="text-muted text-center mb-0 small">Start the conversation.</p>
						</div>`);
    const historyCleared =
      $.parseHTML(`<div class="empty-msg d-block mb-auto bg-light p-2">
						<h6 class="text-center small"><i class="fa fa-history"></i> History was cleared</h6>
						<p class="text-muted text-center mb-0 small">Start over the conversation.</p>
						</div>`);
    if (group) {
      var userMsg = function (msg) {
        return $.parseHTML(`<li class="clearfix">
							<div class="float-end text-end animated--grow-right">
								<div class="message-box sent text-break text-start position-relative px-3 py-2">
									<pre class="m-0">${msg.content}</pre>
                  <p class="fd-dynamicFontSize--tiny ms-auto date mt-1 mb-0">${msg.date_created}</p>
									<div style="box-sizing: border-box; display: flex; position: absolute; right: -6px; bottom: 0px; transform: scaleX(-1);">
										<svg width="6" height="11" viewBox="0 0 6 11" fill="none" xmlns="http://www.w3.org/2000/svg">
											<path d="M-3.05176e-05 10.5019C-3.05176e-05 10.777 0.222986 11 0.49809 11H5.99997V0C5.99997 4.06498 4.64357 7.63316 0.640783 9.52185C0.25977 9.70162 -3.05176e-05 10.0768 -3.05176e-05 10.4981V10.4981L-2.69413e-05 10.5L-3.05176e-05 10.5019V10.5019Z" fill="#ffc530"></path>
										</svg>
									</div>
								</div>
							</div>
						</li>`);
      };
      var partnerMsg = function (msg) {
        return $.parseHTML(`<li class="mb-2">
								<div class="ms-2 text-dark d-inline-flex">
                  <div class="avatar avatar-text">
                    ${msg.author[0]}
                  </div>
								</div><br>
								<div class="message-box text-break group-reply bg-gray-200 mt-1 px-3 py-2">
									<pre class="m-0">${msg.content}</pre>
                  <p class="fd-dynamicFontSize--tiny ms-auto text-muted mt-1 mb-0">${msg.date_created}</p>
								</div>
							</li>`);
      };
    } else {
      var userMsg = function (msg) {
        return $.parseHTML(`<li class="clearfix mb-3">
						<div class="msg-instance float-end text-end animated--grow-right" id="id_msg_${msg.id}">
							<div class="float-start me-2 msg-actions">
								<div class="dropdown">
									<button class="btn btn-circle border shadow" type="button" id="msgActions" data-bs-toggle="dropdown" aria-expanded="false">
										<i class="fa fa-ellipsis"></i>
									</button>
									<ul class="dropdown-menu" aria-labelledby="msgActions">
										<li><a msg-target="#id_msg_${msg.id}" class="dropdown-item small px-2 py-1" href="${msg.replay_url}">Replay</a></li>
										<li><a msg-target="#id_msg_${msg.id}" class="msg-edit dropdown-item small px-2 py-1" href="#">Edit</a></li>
										<li><a msg-target="#id_msg_${msg.id}" class="msg-edit dropdown-item small px-2 py-1" href="#">Copy Text</a></li>
										<li><a msg-target="#id_msg_${msg.id}" class="msg-delete dropdown-item small px-2 py-1 text-danger" href="${msg.delete_url}">Delete</a></li>
									</ul>
								</div>
							</div>
							<div class="message-box sent text-break text-start position-relative px-3 py-2">
								<pre class="msg-content m-0">${msg.content}</pre>
                <p class="fd-dynamicFontSize--tiny ms-auto date mt-1 mb-0">${msg.date_created}</p>
								<div style="box-sizing: border-box; display: flex; position: absolute; right: -6px; bottom: 0px; transform: scaleX(-1);">
									<svg width="6" height="11" viewBox="0 0 6 11" fill="none" xmlns="http://www.w3.org/2000/svg">
										<path d="M-3.05176e-05 10.5019C-3.05176e-05 10.777 0.222986 11 0.49809 11H5.99997V0C5.99997 4.06498 4.64357 7.63316 0.640783 9.52185C0.25977 9.70162 -3.05176e-05 10.0768 -3.05176e-05 10.4981V10.4981L-2.69413e-05 10.5L-3.05176e-05 10.5019V10.5019Z" fill="#ffc530"></path>
									</svg>
								</div>
							</div>
						</div>
						</li>`);
      };
      var partnerMsg = function (msg) {
        return $.parseHTML(`<li class="clearfix mb-3">
						<div class="msg-instance float-start animated--grow-left" id="id_msg_${msg.id}">
							<div class="float-end ms-2 msg-actions">
								<div class="dropdown">
									<button class="btn btn-circle border shadow" type="button" id="msgActions" data-bs-toggle="dropdown" aria-expanded="false">
										<i class="fa fa-ellipsis"></i>
									</button>
									<ul class="dropdown-menu" aria-labelledby="msgActions">
										<li><a msg-target="#id_msg_${msg.id}" class="dropdown-item small px-2 py-1" href="${msg.replay_url}">Replay</a></li>
										<li><a msg-target="#id_msg_${msg.id}" class="msg-edit dropdown-item small px-2 py-1" href="#">Edit</a></li>
										<li><a msg-target="#id_msg_${msg.id}" class="msg-delete dropdown-item small px-2 py-1 text-danger" href="${msg.delete_url}">Delete</a></li>
									</ul>
								</div>
							</div>
							<div class="message-box recieved text-dark text-break bg-gray-300 border position-relative px-3 py-2">
								<pre class="msg-content m-0">${msg.content}</pre>
                <p class="fd-dynamicFontSize--tiny ms-auto text-muted mt-1 mb-0">${msg.date_created}</p>
                </div>
						</div>
						</li>`);
      };
    }
    /*
     * ------------------------------------------------------------------------
     * End variables
     * ------------------------------------------------------------------------
     */

    var next = 1;

    chatBody.on("scroll", function () {
      if (chatBody.scrollTop() <= 30) {
        fetchMessages((next += 1));
        // wait 500 ms before fetching next page
        // setTimeout(function () {console.log("paginating messages")}, 500)
      }
    });

    function total_unread_messages() {
      if (!msg_counter_url === null) {
        $.ajax({
          type: "GET",
          url: msg_counter_url,
          success: function (response) {
            if (response["total_unread_counter"] > 0) {
              $("#total-unread-chat-notifications-counter")
                .parent(".notify-badge")
                .css("display", "block");
              $("#total-unread-chat-notifications-counter").text(
                `${response["total_unread_counter"]}`
              );
            } else {
              $("#total-unread-chat-notifications-counter")
                .parent(".notify-badge")
                .css("display", "none");
            }
          },
          error: function (response) {
            console.log(response);
          },
        });
      }
    }
    total_unread_messages();

    const websocket_url =
      // (window.location.protocol === "https:" ? "wss" : "ws") +
      "ws://" + window.location.host + "/ws/chats/2/";
    // roomName +
    // "/";
    console.log("websocket_url", websocket_url);
    const chatSocket = new ReconnectingWebSocket(websocket_url);
    chatSocket.onopen = function (e) {
      websocketConnected();
      fetchMessages(next);
    };
    chatSocket.onmessage = function (e) {
      onmessage(e);
    };
    chatSocket.onclose = function (e) {
      onclose(e);
    };

    chatSubmit.on("click", function (e) {
      onclick(e);
    });
    msgInput.on("keyup", function (e) {
      onkeyup(e);
    });

    // Load more messages on button click
    loadMoreBtn.on("click", function (e) {
      e.preventDefault();
      $(this).addClass("animated--scale-in-out");
      removeAnim("animated--scale-in-out");
      fetchMessages(parseInt(loadMoreBtn.attr("value")));
    });

    function removeAnim(anim) {
      $(`.${anim}`).on("animationend", function () {
        $(this).removeClass(anim);
      });
    }

    function onmessage(e) {
      const data = JSON.parse(e.data);
      if (data["next_page"] === null) {
        loadMoreBtn.replaceWith("");
      } else {
        loadMoreBtn.html("Load more messages");
        loadMoreBtn.attr("value", data["next_page"]);
      }
      if (data["command"] === "messages") {
        // Check if the room has messages, if not exit with some placeholder text
        if (data["messages"].length === 0) {
          data["history_cleared"]
            ? chatBody.prepend(historyCleared)
            : chatBody.prepend(emptyMessage);
          // if (data['history_cleared']) {
          // 	chatBody.prepend(historyCleared)
          // }
          // else {
          // 	chatBody.prepend(emptyMessage)
          // }
          return;
        }
        // Loop though each message and add to the chat log
        for (let i = 0; i < data["messages"].length; i++) {
          _createMessage(
            data["messages"][i],
            data["command"],
            data["auto_scroll"]
          );
        }
      } else if (data["command"] === "new_message") {
        _createMessage(data["message"], data["command"]);
      }
      total_unread_messages();
    }

    function onclick(e) {
      const message = msgInput.val().trim();
      if (message === "") {
        return;
      }
      chatSocket.send(
        JSON.stringify({
          roomId: roomId,
          command: "new_message",
          message: message,
          from: username,
        })
      );
      msgInput.val("");
      msgInput.trigger("focus");
    }

    function onkeyup(e) {
      if (e.target.value !== "") {
        chatSubmit.addClass("btn-fb-primary");
        chatSubmit.removeAttr("disabled");
      } else {
        chatSubmit.removeClass("btn-fb-primary");
        chatSubmit.attr("disabled", true);
      }
      return;
      if (!group && e.keyCode === 13) {
        // enter, return
        chatSubmit.trigger("click");
      }
    }

    function onclose(e) {
      websocketDisconnected();
      console.error("Chat socket closed unexpectedly");
    }

    var prev = 0;
    function fetchMessages(page) {
      // Check if the message has been loaded already
      if (prev === page) return;

      chatSocket.send(
        JSON.stringify({
          roomId: roomId,
          command: "fetch_messages",
          page: page,
          username: username,
        })
      );
      prev = page;
      total_unread_messages();
    }

    function _createMessage(message, command, autoScroll = true) {
      if (message["author"] === username) {
        var msgEle = userMsg(message);
      } else {
        var msgEle = partnerMsg(message);
      }
      // remove the empty message indicator after new message has been created
      if (chatBody.children(".empty-msg").length > 0) {
        chatBody.children(".empty-msg").remove();
      }
      // append if command is 'new_message', otherwise prepend
      command == "new_message"
        ? chatLog.append(msgEle)
        : chatLog.prepend(msgEle);

      // Scroll to the end of the chat
      if (autoScroll) {
        // For group scroll the html to the bottom
        if (group) {
          $("html").scrollTop(chatLog.height());
        }
        // For thread scroll the chatBody to the end
        chatBody.scrollTop(chatBody.prop("scrollHeight"));
      }
      editMsg();
    }

    $(".msg-delete").click(function (e) {
      e.stopPropagation();
      e.preventDefault();
      $.ajax({
        type: "GET",
        url: $(this).attr("href"),
        success: function (res) {
          console.log(res);
        },
        error: function (res) {
          console.log(res);
        },
      });
    });

    function editMsg() {
      $(".msg-edit").click(function (e) {
        e.stopPropagation();
        e.preventDefault();

        console.log(
          "$($(this).attr('msg-target')).find('.msg-content').text()",
          $($(this).attr("msg-target")).find(".msg-content").text()
        );
        $(msgInput).val(
          $($(this).attr("msg-target")).find(".msg-content").text()
        );
        $(msgInput).trigger("focus");
        // $.ajax({
        // 	type: 'GET',
        // 	url: $(this).attr('href'),
        // 	success: function(res) {
        // 		console.log(res)
        // 	},
        // 	error: function(res) {
        // 		console.log(res)
        // 	}
        // })
      });
    }
  };
})(jQuery);

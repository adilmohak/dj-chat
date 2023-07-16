// ///////////////////
// utility functions to handle different operations
// - request fail
// - websocket connect
// - websocket disconnect
// ///////////////////

// handle when error happen in processing user request
function requestFailHandler(
	error=null,
	msg="Something went wrong while processing your request. \nTry again!",
	refreash=true
) {
	if (error) {
		alert(`ERROR(${error.code}): ${error.message}\n${msg}`);
	}
	alert(msg);
}

// Chat secket closed/disconnected handler
function websocketDisconnected() {
	toastr.warning("WebSocket disconnected. reconnecting...")
}

// Chat secket connected handler
function websocketConnected() {
	toastr.success("WebSocket Connected.")
}

module.exports = {
    requestFailHandler: requestFailHandler,
    websocketDisconnected: websocketDisconnected,
    websocketConnected: websocketConnected,
};

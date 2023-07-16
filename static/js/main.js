// window.open('http://localhost:8000/', 'Order complete', 'width=600, height=600');

// Formats supported: 9xxxxxxxx  09xxxxxxxx 2519xxxxxxxx and +2519xxxxxxxx with spaces, comma, periods, brackets.
// The return value is empty (null) when the format is not supported.
function cleanPhone(num) {
	// First remove any non-digits characters like in 09-12.34.56 78
	var digits=num && num.replace(/[- )(\.]/g,'')
		// Match leading +2519 or 2519 or 09 or 9 followed by exactly 8 digits
		.match(/^(\+?251|0)?9(\d\d\d\d\d\d\d\d)$/)
		// If the string matched, return with prefix +2519
		if(digits && digits[2]) 
			return '+2519'+digits[2]
		return null
}
// Function to show a user a phone number as returned from HelloCash API in local format.
// Simply replaces leading +2519 by 09 
function toLocalPhone(to) {
	return to && to.replace(/^\+2519/,'09')
}

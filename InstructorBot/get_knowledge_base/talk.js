var request = require('request-promise');
async function send_tag() {
	var data = {
		tag:"11FC19",
        c_tag:"11LC16"
	};
    clue="third clue"
    
    if (clue=="first clue"){
        var options = {
            method: 'POST',
            uri: 'http://127.0.0.1:5000/clue_1',
            body: data,
            json: true
        };
    }else if(clue=="second clue"){
        var options = {
            method: 'POST',
            uri: 'http://127.0.0.1:5000/clue_2',
            body: data,
            json: true
        };
    }
    else if(clue=="third clue")
    {
        var options = {
            method: 'POST',
            uri: 'http://127.0.0.1:5000/clue_3',
            body: data,
            json: true
        };
    }
	
	await request(options)

		// The parsedBody contains the data sent back from the Flask server
		.then(function (parsedBody) {
			let result;
			result = parsedBody['result'];
			console.log(result);
		})
		.catch(function (err) {
			console.log(err);
		});
}

send_tag();

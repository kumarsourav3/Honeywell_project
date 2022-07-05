// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
var request = require('request-promise');

const { ActivityHandler, TurnContext, CardFactory , ActionTypes } = require('botbuilder');
const {spawn} = require('child_process');
//const fetch = require('node-fetch');
async function gettaginfopy(user_tag) {
    return promise= new Promise(function(resolve, reject) { 
        var dataToSend;
        //console.log(user_tag);
        // spawn new child process to call the python script
        const python = spawn('python', ['script1.py', user_tag]);
        // collect data from script
        python.stdout.on('data', function (data) {
            //console.log('Pipe data from python script ...');
            dataToSend = data.toString();
        });
        // in close event we are sure that stream from child process is closed
         python.on('close', (code) => {
            //console.log(`child process close all stdio with code ${code}`);
                // send data to browser
            resolve(dataToSend);
        });
         
    })
}
/*
This function posts a request to flask server running at 'http://127.0.0.1:5000/tag' and returns the name of 
tag which should be under action at the step of an exercise
*/

async function get_tag_name(exercise_no, order) {

	// This variable contains the data you want to send
	var data = {
		'exercise_no': exercise_no,
        'order': order
	}
    console.log(exercise_no);

	var options = {
		method: 'POST',
        // http:flaskserverurl:port/route
		uri: 'http://127.0.0.1:5000/tag',
		body: data,
        // Automatically stringifies the body to JSON
		json: true
	};

	var sendrequest2;
    await request(options)

		// The parsedBody contains the data
		// sent back from the Flask server
		.then(function (parsedBody) {
			console.log(parsedBody);
			let result;
			result = parsedBody['result'];
            sendrequest2 = result;
			console.log(result);
		})
		.catch(function (err) {
			console.log(err);
		});
    return sendrequest2;
}
/*
This function posts a request to flask server running at 'http://127.0.0.1:5000/description' and returns the 
description of step to be performed.
*/

async function get_procedure_description(exercise_no, order) {

	// This variable contains the data you want to send
	var data = {
		'exercise_no':exercise_no,
        'order': order
	}
	var options = {
		method: 'POST',
        // http:flaskserverurl:port/route
		uri: 'http://127.0.0.1:5000/description',
		body: data,
        // Automatically stringifies the body to JSON
		json: true
	};

	var sendrequest;
    await request(options)

		// The parsedBody contains the data
		// sent back from the Flask server
		.then(function (parsedBody) {
			console.log(parsedBody);
			let result;
			result = parsedBody['result'];
            sendrequest = result;
            // console.log(sendrequest);
			// console.log(result);
		})
		.catch(function (err) {
			console.log(err);
		});
    return sendrequest;
}

/*
This function posts a request to flask server running at 'http://127.0.0.1:5000/' and returns the clue 
that has been requested by trainee
*/


async function send_tag(clue,tag_) {
	var data = {
		tag:tag_,
        // c_tag:"11LC16"
	};
    //clue="third clue"
    
    if (clue=="first"){
        var options = {
            method: 'POST',
            uri: 'http://127.0.0.1:5000/clue_1',
            body: data,
            json: true
        };
    }else if(clue=="second"){
        var options = {
            method: 'POST',
            uri: 'http://127.0.0.1:5000/clue_2',
            body: data,
            json: true
        };
    }
    else if(clue=="third")
    {
        var options = {
            method: 'POST',
            uri: 'http://127.0.0.1:5000/clue_3',
            body: data,
            json: true
        };
    }
	var sendrequest;
	await request(options)

		// The parsedBody contains the data sent back from the Flask server
		.then(function (parsedBody) {
			let result;
			result = parsedBody['result'];
			console.log(result);

            sendrequest = result;
		})
		.catch(function (err) {
			console.log(err);
		});
   // return result;

  // console.log(sendrequest);
   return sendrequest;
}

class ProactiveBot extends ActivityHandler {
    constructor(conversationReferences) {
        super();

        // Dependency injected dictionary for storing ConversationReference objects used in NotifyController to proactively message users
        this.conversationReferences = conversationReferences;

        this.onConversationUpdate(async (context, next) => {
            this.addConversationReference(context.activity);

            await next();
        });
        var counter;
        this.onMembersAdded(async (context, next) => {
            const reply = { type: ActionTypes.Message };
            const buttons = [
                { type: ActionTypes.PostBack, title: 'Exercise 7.1', value: '7.1' },
                { type: ActionTypes.PostBack, title: 'Exercise 7.2', value: '7.2' },
                { type: ActionTypes.PostBack, title: 'Exercise 7.3', value: '7.3' },
                { type: ActionTypes.PostBack, title: 'Exercise 7.4', value: '7.4' },
                { type: ActionTypes.PostBack, title: 'Exercise 7.5', value: '7.5' },
                { type: ActionTypes.PostBack, title: 'Exercise 7.6', value: '7.6' },
                { type: ActionTypes.PostBack, title: 'Exercise 7.7', value: '7.7' },
                { type: ActionTypes.PostBack, title: 'Exercise 7.8', value: '7.8' }
            ];
            counter = 1;
            const card = CardFactory.heroCard('', undefined,
                buttons, { text: 'Hi ! Welcome to the Instructor Bot. Which exercise do you want to take?' });
            reply.attachments = [card];
            
            const membersAdded = context.activity.membersAdded;
            for (let cnt = 0; cnt < membersAdded.length; cnt++) {
                if (membersAdded[cnt].id !== context.activity.recipient.id) {
                    const welcomeMessage = 'Hi ! Welcome to the Instructor Bot. ';
                    await context.sendActivity(reply);
                }
            }

            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });
        var exercise_no;
        var clue_no;
        this.onMessage(async (context, next) => {
            this.addConversationReference(context.activity);
            
            const message = context.activity.text
            
            console.log(counter);
            var regexp = /^\d+\.\d{0,2}$/;
           
            if(message=="done"){
                counter = counter + 1;
                const reply1 = await get_procedure_description(exercise_no, counter);
                await context.sendActivity( reply1 );
            }
            if(regexp.test(message)){
                exercise_no = message;
                counter =1
                const v = await get_procedure_description(exercise_no, counter);
                const replyText = "Starting exercise "+ message +".\nIf you have done changes in the PTS application, reply done, else reply need help.";
                await context.sendActivity( replyText );
                await context.sendActivity( v);
            }
            
           
            if(message == "need help"){
                const reply = { type: ActionTypes.Message };
                const buttons = [
                    { type: ActionTypes.PostBack, title: 'Clue 1 : The correct tag', value: 'first' },
                    { type: ActionTypes.PostBack, title: 'Clue 2 : Description of correct tag',value: 'second' },
                    { type: ActionTypes.PostBack, title: 'Clue 3 : Range of the values where the value of tag should lie', value: 'third' }
                ];
        
                const card = CardFactory.heroCard('', undefined,
                    buttons, { text: 'We can help you by providing the following three clues. Which clue do you want to take?' });
                reply.attachments = [card];
                console.log("inside need help");
                await context.sendActivity( reply );
               
            }
            if(message=="first" || message=="second" || message=="third"){
                clue_no=message;
                const tag= await get_tag_name(exercise_no,counter)
                const replyText = await send_tag(clue_no,tag);
                await context.sendActivity( replyText );
            }
            
            //console.log(clue_no);
            
                    // Echo back what the user said
            
            //console.log(replyText);
           
            await next();
        });
    }

    addConversationReference(activity) {
        const conversationReference = TurnContext.getConversationReference(activity);
        this.conversationReferences[conversationReference.conversation.id] = conversationReference;
    }
}

module.exports.ProactiveBot = ProactiveBot;
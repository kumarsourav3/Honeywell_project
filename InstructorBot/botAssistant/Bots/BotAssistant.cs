// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using BotAssistant.Utilities;

namespace Microsoft.BotBuilderSamples
{
    public class BotAssistant : ActivityHandler
    {
        // Message to send to users when the bot receives a Conversation Update event
        private const string WelcomeMessage = "Welcome to the Bot Assistant.";

        // Dependency injected dictionary for storing ConversationReference objects used in EventController
        private readonly ConcurrentDictionary<string, ConversationReference> _conversationReferences;

        public BotAssistant(ConcurrentDictionary<string, ConversationReference> conversationReferences)
        {
            _conversationReferences = conversationReferences;
        }

        private void AddConversationReference(Activity activity)
        {
            var conversationReference = activity.GetConversationReference();
            _conversationReferences.AddOrUpdate(conversationReference.User.Id, conversationReference, (key, newValue) => conversationReference);
        }

        protected override Task OnConversationUpdateActivityAsync(ITurnContext<IConversationUpdateActivity> turnContext, CancellationToken cancellationToken)
        {
            AddConversationReference(turnContext.Activity as Activity);

            return base.OnConversationUpdateActivityAsync(turnContext, cancellationToken);
        }

        protected override async Task OnMembersAddedAsync(IList<ChannelAccount> membersAdded, ITurnContext<IConversationUpdateActivity> turnContext, CancellationToken cancellationToken)
        {
            foreach (var member in membersAdded)
            {
                // Greet anyone that was not the target (recipient) of this message.
                if (member.Id != turnContext.Activity.Recipient.Id)
                {
                    await turnContext.SendActivityAsync(MessageFactory.Text(WelcomeMessage), cancellationToken);
                }
            }
        }

        protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            AddConversationReference(turnContext.Activity as Activity);
            Utilities.GetTagDetail(turnContext.Activity.Text);
            if(!string.IsNullOrEmpty(Utilities.TagDetail?.Tag))
            {
                // Tag Detail for the input Tag Name
                await turnContext.SendActivityAsync(MessageFactory.Text($"TagInformation:\n" +
                 $"TagName: {Utilities.TagDetail.Tag}\n" +
                 $"TagInfo: {Utilities.TagDetail.Info}\n" +
                 $"LowLimit:{Utilities.TagDetail.LowLimit}\n" +
                 $"HighLimit:{Utilities.TagDetail.HighLimit}"),cancellationToken);
            }
        }
    }
}

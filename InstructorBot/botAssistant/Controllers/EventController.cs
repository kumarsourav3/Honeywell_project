// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

using System;
using System.Collections.Concurrent;
using System.Net;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Builder.Integration.AspNet.Core;
using Microsoft.Bot.Schema;
using Microsoft.Extensions.Configuration;
using BotAssistant.Enitites;

namespace BotAssistant.Controllers
{
    [Route("api/event")]
    [ApiController]
    public class EventController : ControllerBase
    {
        private readonly IBotFrameworkHttpAdapter _adapter;
        private readonly string _appId;
        private readonly ConcurrentDictionary<string, ConversationReference> _conversationReferences;

        public EventController(IBotFrameworkHttpAdapter adapter, IConfiguration configuration, ConcurrentDictionary<string, ConversationReference> conversationReferences)
        {
            _adapter = adapter;
            _conversationReferences = conversationReferences;
            _appId = configuration["MicrosoftAppId"] ?? string.Empty;
        }

        [HttpPost]
        public async Task<IActionResult> PostAsync([FromBody]EventInfo eventInfo)
        {

            Utilities.Utilities.EventInfo = eventInfo;
            foreach (var conversationReference in _conversationReferences.Values)
            {
                await ((BotAdapter)_adapter).ContinueConversationAsync(_appId, conversationReference, BotCallback, default(CancellationToken));
            }

            // Let the caller know proactive messages have been sent
            return new ContentResult()
            {
                Content = $"{eventInfo.Description}",
                ContentType = "text/html",
                StatusCode = (int)HttpStatusCode.OK,
            };
        }
        private async Task BotCallback(ITurnContext turnContext, CancellationToken cancellationToken)
        {
            Utilities.Utilities.GetTagDetail();

            //TODO: below code is for debugging.Can be removed.
            //Latest Event Info
            await turnContext.SendActivityAsync($"EventInformation:\n" +
                $"TagName: {Utilities.Utilities.EventInfo.TagName}\n" +
                $"TagAndParam: {Utilities.Utilities.EventInfo.TagAndParam}\n" +
                $"Description:{Utilities.Utilities.EventInfo.Description}\n" +
                $"CurrentValue:{Utilities.Utilities.EventInfo.CurrentValue}");

            //TODO: below code is for debugging.Can be removed.
            //Tag Affected
            await turnContext.SendActivityAsync(MessageFactory.Text($"TagInformation:\n" +
                 $"TagName: {Utilities.Utilities.TagDetail.Tag}\n" +
                 $"TagInfo: {Utilities.Utilities.TagDetail.Info}\n" +
                 $"LowLimit:{Utilities.Utilities.TagDetail.LowLimit}\n" +
                 $"HighLimit:{Utilities.Utilities.TagDetail.HighLimit}"), cancellationToken);
        }
    }
}
using BotAssistant.Enitites;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;

namespace BotAssistant.Utilities
{
    public class Utilities
    {
        public static EventInfo EventInfo { get; set; } 
        public static TagDetail TagDetail { get; private set; }
        public static void GetTagDetail(string tagName=null)
        {
            TagDetail = new TagDetail();
            tagName ??= EventInfo.TagName;//If tagName is not passed as input , take EventInfo.TagName //TODO: replace with tagName with latest code
            using (StreamReader r = new StreamReader("tag_info.json"))
            {
                string json = r.ReadToEnd();
                TagDetail = JsonSerializer.Deserialize<List<TagDetail>>(json)?.FirstOrDefault(x=>x.Tag==tagName);
            }
        }
    }
}

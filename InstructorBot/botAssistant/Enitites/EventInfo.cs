using System;

namespace BotAssistant.Enitites
{
    public class EventInfo
    {
        public string TagName { get; set; }
        public string TagAndParam { get; set; }
        public string Description { get; set; }
        public object CurrentValue { get; set; }
        public string SimulationTime { get; set; }
    }
}

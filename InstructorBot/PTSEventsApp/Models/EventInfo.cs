using MongoDB.Bson;

namespace PTSEventsApp.Models
{
    
    public class EventInfo
    {
        public ObjectId Id { get; set; }
        public int EventId { get; set; }
        public string TagName { get; set; }
        public string TagAndParam { get; set; }
        public string Description { get; set; }
        public object CurrentValue { get; set; }
        public string SimulationTime { get; set; }
    }
}

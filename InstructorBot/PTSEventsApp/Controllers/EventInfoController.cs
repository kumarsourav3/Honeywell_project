using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using PTSEventsApp.Models;

namespace PTSEventsApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class EventInfoController : ControllerBase
    {
        private readonly IConfiguration _configuration;
        public EventInfoController(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        [HttpGet]
        public JsonResult Get()
        {
            MongoClient dbClient = new MongoClient(_configuration.GetConnectionString("dbConnection"));

            var dbList = dbClient.GetDatabase("testdb").GetCollection<EventInfo>("EventInfo").AsQueryable();

            return new JsonResult(dbList);
        }

        [HttpPost]
        public JsonResult Post(EventInfo eventInfo)
        {
            MongoClient dbClient = new MongoClient(_configuration.GetConnectionString("dbConnection"));

            int LastEventInfoId = dbClient.GetDatabase("testdb").GetCollection<EventInfo>("EventInfo").AsQueryable().Count();
            eventInfo.EventId = LastEventInfoId + 1;

            dbClient.GetDatabase("testdb").GetCollection<EventInfo>("EventInfo").InsertOne(eventInfo);

            return new JsonResult("Added Successfully");
        }
    }
}
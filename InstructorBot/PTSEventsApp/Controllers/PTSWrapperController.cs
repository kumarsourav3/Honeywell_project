using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Text;
using System.Text.Json;
namespace PTSEventsApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PTSWrapperController : ControllerBase
    {
        private readonly IConfiguration _configuration;
        public PTSWrapperController(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        [HttpPost]
        public async Task<IActionResult> Post(EventInfoDTO eventInfo)
        {

            HttpClient client = new HttpClient
            {
                BaseAddress = new Uri(_configuration.GetValue<string>("BaseAddress"))
            };

            var content = new StringContent(JsonSerializer.Serialize(eventInfo), Encoding.UTF8, "application/json");
            using (HttpResponseMessage response = await client.PostAsync("event", content))
            {
                var responseContent = response.Content.ReadAsStringAsync().Result;
                response.EnsureSuccessStatusCode();

                return Ok(responseContent);
            }
        }
    }
    public class EventInfoDTO
    {
        public string TagName { get; set; }
        public string TagAndParam { get; set; }
        public string Description { get; set; }
        public object CurrentValue { get; set; }
        public string SimulationTime { get; set; }
    }
}

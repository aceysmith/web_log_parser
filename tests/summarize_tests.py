import unittest
import web_log_parser.__main__ as parser

class WebLogParserSummarizeTest(unittest.TestCase):
  def testTransformsSummary(self):
    parsed_logs = {
      '12345': {
        'count': 6789,
        'user_agent_frequency': {
          'user agent 4': 20,
          'user agent 2': 40,
          'user agent 1': 50,
          'user agent 3': 30,
          'user agent 5': 10
        },
        'os_request_method_frequency': {
          'os 1': {
            'GET': 10
          },
          'os 2': {
            'POST': 10,
          },
          'os 3': {
            'GET': 10,
            'POST': 5,
          },
        }
      }
    }
    summary = parser.summarize(parsed_logs)

    self.assertEqual(summary, {
      '12345': {
        'count': 6789,
        'top_user_agents': [
          'user agent 1',
          'user agent 2',
          'user agent 3',
        ],
        'os_get_to_post_ratio': {
          'os 1': 'Infinite',
          'os 2': 0,
          'os 3': 2,
        }
      }
    })

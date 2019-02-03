import re
import sys
import json
from datetime import datetime
from user_agents import parse as user_agent_parse

def parse(filename):
  total_lines = 0
  summary_by_day = {}

  reg_exp = re.compile('(([0-9]+\.?)+) - - \[([^]]+)\] "([^"]+)" (\d+) (\d+) "([^"]*)" "([^"]*")')
  with open(filename, 'r') as file:
    for line in file:
      total_lines += 1
      match = reg_exp.match(line)

      if not match:
        continue

      match_date = match.group(3)
      match_request = match.group(4)
      match_user_agent = match.group(8)

      request_parts = match_request.split(' ')
      if len(request_parts) == 0:
        continue
      request_method = request_parts[0]

      user_agent = user_agent_parse(match_user_agent)
      os = user_agent_parse(match_user_agent).os.family

      try:
        date = datetime.strptime(match_date, '%d/%b/%Y:%H:%M:%S %z')
      except ValueError as e:
        continue

      date_string = str(date.date())
      summary = summary_by_day.get(date_string, {
        'count': 0,
        'user_agent_frequency': {},
        'os_request_method_frequency': {}
      })

      summary['count'] += 1

      summary['user_agent_frequency'][match_user_agent] = 1 + summary['user_agent_frequency'].get(match_user_agent, 0)

      os_request_method_frequency = summary['os_request_method_frequency'].get(os, {})
      os_request_method_frequency[request_method] = 1 + os_request_method_frequency.get(request_method, 0)
      summary['os_request_method_frequency'][os] = os_request_method_frequency

      summary_by_day[date_string] = summary

  return summary_by_day

def summarize(log_summary_by_day):
  summary_by_day = {}
  for day in log_summary_by_day:
    log_summary = log_summary_by_day[day]

    user_agent_frequency = log_summary['user_agent_frequency']
    top_user_agents = sorted(user_agent_frequency, key=user_agent_frequency.get, reverse=True)[0:3]

    os_get_to_post_ratio = {}
    for os in log_summary['os_request_method_frequency']:
      request_method_frequency = log_summary['os_request_method_frequency'][os]
      get_requests = request_method_frequency.get('GET', 0)
      post_requests = request_method_frequency.get('POST', 0)
      if post_requests == 0:
        os_get_to_post_ratio[os] = 'Infinite'
      else:
        os_get_to_post_ratio[os] = get_requests / post_requests

    summary_by_day[day] = {
      'count': log_summary['count'],
      'top_user_agents': top_user_agents,
      'os_get_to_post_ratio': os_get_to_post_ratio,
    }

  return summary_by_day


def display(summary_by_day):
  for day in summary_by_day:
    summary = summary_by_day[day]
    print('Day: ', day)
    print('  Requests: ', summary['count'])
    print('  Top User Agents:')
    for user_agent in summary['top_user_agents']:
      print('    ', user_agent)
    print('  OS GET/POST Ratio:')
    for os in summary['os_get_to_post_ratio']:
      ratio = summary['os_get_to_post_ratio'][os]
      print('    ', os, ': ', ratio)


def main():
  parsed_logs = parse(sys.argv[1])
  summary = summarize(parsed_logs)
  display(summary)

if __name__ == '__main':
  main()

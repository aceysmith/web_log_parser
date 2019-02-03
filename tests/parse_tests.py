import unittest
import web_log_parser.__main__ as parser

class WebLogParserSummarizeTest(unittest.TestCase):
  def testValidatesFormat(self):
    summary = parser.parse('tests/logs/validates_format.log')

    self.assertEqual(summary['2011-12-01']['count'], 1)

  def testValidatesDateFormat(self):
    summary = parser.parse('tests/logs/validates_date_format.log')

    self.assertEqual(summary['2011-12-01']['count'], 1)

  def testAggregatesDates(self):
    summary = parser.parse('tests/logs/aggregates_dates.log')

    self.assertEqual(summary['2011-12-01']['count'], 2)

  def testDetectsOSes(self):
    summary = parser.parse('tests/logs/detects_oses.log')

    self.assertEqual(len(summary['2011-12-01']['os_request_method_frequency']), 3)

  def testValidatesRequestFormat(self):
    summary = parser.parse('tests/logs/validates_request_format.log')

    self.assertEqual(summary['2011-12-01']['count'], 1)

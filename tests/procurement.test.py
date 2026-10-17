"""Check procurement placement and honest no-update rendering."""
import copy, importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('build',Path(__file__).resolve().parents[1]/'scripts/build.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)

class ProcurementTests(unittest.TestCase):
 def setUp(self):
  self.issue={'report_date':'2026-10-18','items':[{'information_type':'paper'}], 'procurement_status':{'status':'no_verified_updates','title_cn':'采购与需求动态','summary_cn':'本期未检索到新增已核实公告。已查中国及海外公开来源；部分页面未读到正文。<script>bad</script>','checked_at':'2026-10-18T08:00:00+08:00','registered_candidates':3}}
 def test_empty_state_is_visible_escaped_and_not_an_announcement(self):
  build.validate_procurement(self.issue);s=build.procurement_status_html(self.issue)
  self.assertIn('采购与需求动态',s);self.assertIn('02<span>',s)
  self.assertIn('&lt;script&gt;',s);self.assertNotIn('<script>',s);self.assertNotIn('<article',s)
  self.assertEqual(len(self.issue['items']),1)
 def test_missing_status_is_rejected(self):
  self.issue.pop('procurement_status')
  with self.assertRaises(AssertionError):build.validate_procurement(self.issue)
 def test_one_combined_tender_must_be_last(self):
  self.issue.pop('procurement_status');self.issue['items'].append({'information_type':'tender'})
  build.validate_procurement(self.issue);self.assertEqual(build.procurement_status_html(self.issue),'')
  self.issue['items'].reverse()
  with self.assertRaises(AssertionError):build.validate_procurement(self.issue)
 def test_tender_cannot_coexist_with_no_update_status(self):
  self.issue['items'].append({'information_type':'tender'})
  with self.assertRaises(AssertionError):build.validate_procurement(self.issue)
 def test_check_date_uses_shanghai_day(self):
  self.issue['procurement_status']['checked_at']='2026-10-17T23:59:59+00:00'
  build.validate_procurement(self.issue)
  self.issue['procurement_status']['checked_at']='2026-10-17T15:59:59+00:00'
  with self.assertRaises(AssertionError):build.validate_procurement(self.issue)
 def test_old_issues_remain_compatible(self):
  old={'report_date':'2026-10-16','items':[{'information_type':'paper'}]}
  build.validate_procurement(old);self.assertEqual(build.procurement_status_html(old),'')

if __name__=='__main__':unittest.main()

#!/usr/bin/env python3
"""
GitHub Actions ワークフロー可視化ツール
リポジトリのワークフロー実行状況をアスキーアートで表示します
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Any

class WorkflowVisualizer:
    def __init__(self):
        self.colors = {
            'success': '\033[92m',
            'failure': '\033[91m',
            'in_progress': '\033[93m',
            'cancelled': '\033[94m',
            'skipped': '\033[90m',
            'reset': '\033[0m'
        }
    
    def run_gh_command(self, cmd: List[str]) -> Dict[str, Any]:
        """GitHub CLIコマンドを実行"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"エラー: {e}")
            return {}
        except json.JSONDecodeError:
            print("JSONデコードエラー")
            return {}
    
    def get_workflow_runs(self, limit: int = 10) -> List[Dict]:
        """最新のワークフロー実行結果を取得"""
        cmd = ['gh', 'run', 'list', '--limit', str(limit), '--json', 
               'status,conclusion,workflowName,createdAt,headBranch']
        return self.run_gh_command(cmd)
    
    def get_status_symbol(self, status: str, conclusion: str) -> str:
        """ステータスに応じたシンボルを返す"""
        if status == 'completed':
            if conclusion == 'success':
                return f"{self.colors['success']}✓{self.colors['reset']}"
            elif conclusion == 'failure':
                return f"{self.colors['failure']}✗{self.colors['reset']}"
            elif conclusion == 'cancelled':
                return f"{self.colors['cancelled']}○{self.colors['reset']}"
            elif conclusion == 'skipped':
                return f"{self.colors['skipped']}−{self.colors['reset']}"
        elif status == 'in_progress':
            return f"{self.colors['in_progress']}⟳{self.colors['reset']}"
        return "?"
    
    def create_progress_bar(self, runs: List[Dict]) -> str:
        """実行結果をプログレスバー風に表示"""
        symbols = []
        for run in runs:
            symbol = self.get_status_symbol(run['status'], run.get('conclusion', ''))
            symbols.append(symbol)
        
        return f"[{''.join(symbols)}]"
    
    def display_workflow_tree(self, runs: List[Dict]):
        """ワークフローをツリー形式で表示"""
        print("\n🌳 GitHub Actions ワークフロー実行状況")
        print("=" * 50)
        
        workflows = {}
        for run in runs:
            workflow_name = run['workflowName']
            if workflow_name not in workflows:
                workflows[workflow_name] = []
            workflows[workflow_name].append(run)
        
        for workflow_name, workflow_runs in workflows.items():
            print(f"\n📋 {workflow_name}")
            progress_bar = self.create_progress_bar(workflow_runs[:10])
            print(f"   {progress_bar}")
            
            for i, run in enumerate(workflow_runs[:5]):
                symbol = self.get_status_symbol(run['status'], run.get('conclusion', ''))
                branch = run.get('headBranch', 'unknown')
                created_at = run.get('createdAt', '')
                
                if created_at:
                    try:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        time_str = dt.strftime('%m/%d %H:%M')
                    except:
                        time_str = created_at[:10]
                else:
                    time_str = 'unknown'
                
                prefix = "├── " if i < len(workflow_runs) - 1 else "└── "
                print(f"   {prefix}{symbol} {branch} ({time_str})")
    
    def display_statistics(self, runs: List[Dict]):
        """統計情報を表示"""
        if not runs:
            return
        
        stats = {'success': 0, 'failure': 0, 'cancelled': 0, 'in_progress': 0}
        
        for run in runs:
            if run['status'] == 'completed':
                conclusion = run.get('conclusion', 'unknown')
                if conclusion in stats:
                    stats[conclusion] += 1
            elif run['status'] == 'in_progress':
                stats['in_progress'] += 1
        
        total = len(runs)
        print(f"\n📊 統計情報 (直近{total}件)")
        print("-" * 30)
        
        for status, count in stats.items():
            if count > 0:
                percentage = (count / total) * 100
                bar_length = int(percentage / 5)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                color = self.colors.get(status, '')
                reset = self.colors['reset']
                print(f"{color}{status:12}{reset} {bar} {count:2d} ({percentage:5.1f}%)")
    
    def display_ascii_art(self):
        """アスキーアートを表示"""
        art = """
    ⚡ GitHub Actions Monitor ⚡
    
         🤖
        /|||\\
       ( o.o )
        > ^ <
        
    ワークフロー実行状況をお知らせします！
        """
        print(art)
    
    def run(self):
        """メイン実行関数"""
        self.display_ascii_art()
        
        print("GitHub CLIでワークフロー情報を取得中...")
        runs = self.get_workflow_runs(20)
        
        if not runs:
            print("❌ ワークフロー情報を取得できませんでした")
            print("💡 'gh auth login' でGitHubにログインしてください")
            return
        
        self.display_workflow_tree(runs)
        self.display_statistics(runs)
        
        print(f"\n🔗 詳細情報: gh run list")
        print("=" * 50)

if __name__ == "__main__":
    visualizer = WorkflowVisualizer()
    visualizer.run()
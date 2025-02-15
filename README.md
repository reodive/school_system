# SmartLearn

## プロジェクト概要
- Django を使用した学校向け学習管理システムです。
- 課題管理、ユーザー管理、グループ（クラス）管理、お知らせ機能、Google Calendar 連携機能を提供します。

## 構成
- **school_system/**: プロジェクト設定（settings.py, urls.py など）
- **tasks/**: 課題管理、お知らせ機能、Google Calendar 連携機能
- **users/**: カスタムユーザー管理、認証、グループ管理
- **templates/**: 共通レイアウトおよび各種テンプレート
- **venv/**: Python 仮想環境

## セットアップ方法
1. 仮想環境を作成して有効化します。
   ```bash
   python -m venv venv
   venv\Scripts\activate

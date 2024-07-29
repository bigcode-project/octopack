from difflib import SequenceMatcher
from multiprocessing import Pool, Value
import os
import random
import re
import shutil

import datasets
from huggingface_hub import login

import numpy as np

#login()
# Most common natural languages in The Stack
GOOD_STARTS_EN = {'troubleshoot', 'indent', 'eradicate', 'allow', 'access', 'augment', 'load', 'join', 'accelerate', 'mark', 'generalize', 'disable', 'allot', 'stipulate', 'mend', 'merge', 'determine', 'speed up', 'rearrange', 'rectify', 'prepare', 'cut', 'edit', 'choose', 'destroy', 'hasten', 'hide', 'gather', 'facilitate', 'uncover', 'detach', 'select', 'enumerate', 'clone', 'duplicate', 'cover', 'install', 'uninstall', 'read', 'structure', 'recompile', 'debug', 'transform', 'orchestrate', 'develop', 'recomment', 'reset', 'validate', 'automate', 'indent', 'refresh', 'backup', 'replace', 'deal with', 'scrub', 'improve', 'terminate', 'monitor', 'revise', 'solve', 'decipher', 'amplify', 'reshape', 'sort', 'boost', 'split', 'adjust', 'designate', 'unstage', 'unwind', 'halt', 'downgrade', 'handle', 'decommission', 'unify', 'add', 'reimplement', 'connect', 'archive', 'interrupt', 'discard', 'compress', 'index', 'initialize', 'streamline', 'interpolate', 'format', 'append', 'delete', 'consolidate', 'brush up', 'settle', 'annotate', 'include', 'unblock', 'break', 'update', 'change', 'switch', 'reorganize', 'fix', 'reannotate', 'tackle', 'transpose', 'prepend', 'increase', 'paraphrase', 'integrate', 'order', 'reschedule', 'scale', 'maintain', 'reinforce', 'truncate', 'drop', 'abort', 'remove', 'configure', 'unplug', 'save', 'create', 'reformat', 'advance', 'rework', 'concatenate', 'decrypt', 'rewrite', 'check', 'divide', 'relocate', 'complete', 'dismantle', 'clarify', 'restructure', 'isolate', 'rollback', 'comment', 'send', 'standardize', 'untangle', 'disentangle', 'unravel', 'streamline', 'clean', 'decompress', 'reduce', 'decomplexify', 'reword', 'provision', 'reorder', 'revoke', 'embed', 'redact', 'store', 'extend', 'unsync', 'return', 'optimize', 'align', 'test', 'reposition', 'expand', 'leverage', 'enlarge', 'inflate', 'escalate', 'package', 'simplify', 'tidy', 'establish', 'stabilize', 'expire', 'deploy', 'plug ', 'reboot', 'enhance', 'attach', 'decrease', 'declare', 'rename', 'patch', 'print', 'rebuild', 'synchronize', 'strengthen', 'emphasize', 'diminish', 'trim', 'accumulate', 'work', 'apply', 'copy', 'customize', 'expedite', 'magnify', 'call', 'purge', 'quit', 'unpublish', 'throw', 'watch', 'clear', 'implement', 'define', 'make', 'watermark', 'raise', 'stop', 'substitute', 'normalize', 'rephrase', 'undo', 'paste', 'whitelist', 'mask', 'secure', 'rebase', 'set', 'tag', 'encrypt', 'reconnect', 'repackage', 'exit', 'arrange', 'build', 'migrate', 'swap', 'bring', 'bump', 'tweak', 'upgrade', 'write', 'resolve', 'put', 'exclude', 'insert', 'kill', 'subtract', 'repair', 'revert', 'redefine', 'enforce', 'convert', 'multiply', 'use', 'enable', 'support', 'document', 'correct', 'withdraw', 'move', 'modify', 'allot', 'introduce', 'address', 'increment', 'manage', 'verify', 'reconfigure', 'refactor'}
GOOD_STARTS_ZH = {'把', '替换', '降级', '保存', '修改', '解压缩', '撤销拉取', '修复', '对齐', '处理', '准备', '验证', '应用', '设置', '制作', '加速', '校正', '补丁', '重新调度', '重新配置', '重新实现', '更改', '复制', '评论', '增强', '合并', '编排', '配置', '完成', '部署', '退出', '备份', '回滚', '迁移', '添加', '减去', '重新排列', '重构', '重新定义', '拆分', '抛出', '串联', '简化流程', '终止', '取消暂存', '返回', '重新注释', '标记', '重新排序', '插入', '插值', '修', '定制', '加密', '排除', '重写', '监控', '格式化', '撤销', '放弃', '掩码', '重新连接', '重新组织', '清除', '追加', '停止', '建立索引', '解', '澄清', '微调', '重命名', '结束', '执行', '缩放', '取消发布', '乘以', '撤销暂存区的文件', '改善', '丢弃', '归档', '重新编译', '解除同步', '注释', '解决', '拔掉', '包含', '简化', '清理', '变基', '删除', '同步', '介绍', '存档', '隔离', '调试', '重新格式化', '重新定位', '中断', '转换', '结构化', '过期', '纠正', '刷新', '构建', '截断', '粘贴', '管理', '重新表述', '启用', '整理', '改写', '支持', '文档化', '压缩', '检查', '白名单', '重新打包', '水印', '提高', '改进', '整合', '扩展', '升级', '重置', '移动', '重建', '升级版本', '自动化', '测试', '修剪', '还原', '解除阻止', '剪切', '解决问题', '禁用', '修订', '维护', '解密', '标准化', '初始化', '重新构建', '重启', '打包', '分割', '更新', '安全', '优化', '版本', '重新评论', '实现'}
GOOD_STARTS_FR = {'réinitialise', 'personnalise', 'masque', 'supporte', 'range', 'augmente', 'ajoute', 'liste blanche', 'structure', 'recompile', 'révise', 'désindexe', 'répare', 'retourne', 'soustrais', 'jette', 'complète', 'découpe', 'réimplémente', 'recommande', 'annote', 'débloque', 'indente', 'tague', 'réécris', 'sauvegarde', 'archive', 'reconnecte', 'supprime', 'vérifie', 'reconstruit', 'débranche', 'révoque', 'fabrique', 'refactorise', 'incrémente', 'désynchronise', 'prépare', 'change', 'dépanne', 'migre', 'implémente', 'introduit', 'édite', 'renomme', 'construis', 'ajoute un filigrane', 'convertit', 'travaille', 'configure', 'rectifie', 'clarifie', 'fournis', 'traite', 'transforme', 'aligne', 'sauve', 'réordonne', 'débogue', 'soulève', 'restructure', 'casse', 'reformule', 'modifie', 'rebases', 'prépend', 'réorganise', 'insère', 'rend anonyme', 'nettoie', 'chiffre', 'reconditionne', 'active', 'concatène', 'expire', 'définis', 'valide', 'formate', 'patche', 'compresse', 'commente', 'ordonne', 'fusionne', 'décompresse', 'normalise', 'emballe', 'repositionne', 'documente', 'applique', 'résous', 'met', 'maintient', 'résout', 'tronque', 'déplace', 'impose', 'désactive', 'réarrange', 'purge', 'isole', 'annule', 'corrige', 'arrête', 'adresse', 'multiplie', 'touche à', 'coupe', 'attaque', 'déploie', 'imprime', 'redéfinit', 'revient en arrière', 'échelle', 'régresse', 'unifie', 'ré-annote', 'exclue', 'améliore', 'rafraîchis', 'stocke', 'décrypte', 'colle', 'défait', 'remplace', 'automatise', 'simplifie', 'termine', 'reformate', 'branche', 'consolide', 'synchronise', 'redémarre', 'teste', 'tue', 'met à jour', 'divise', 'copie', 'défait le pull', 'gère', 'dépublie', 'intègre', 'étends', 'utilise', 'optimise', 'inclue', 'sécurise', 'retravaille', 'reviens en arrière', 'accélère', 'interpole', 'surveille', 'reconfigure', 'initialise', 'quitte', 'généralise', 'orchestre'}
GOOD_STARTS_ES = {'detiene', 'repara', 'revoca', 'reposiciona', 'termina', 'reconecta', 'depura', 'renombra', 'desbloquea', 'mejora', 'extiende', 'trabaja', 'aumenta', 'reorganiza', 'integra', 'reconstruye', 'eleva', 'documenta', 'transforma', 'devuelve', 'interpola', 'fusiona', 'implementa', 'rebasa', 'versiona', 'alinea', 'reimplementa', 'cifra', 'mantiene', 'prueba', 'refactoriza', 'toca', 'gestiona', 'sincroniza', 'rompe', 'migra', 'almacena', 'comprime', 'indenta', 'estructura', 'dessincroniza', 'incrementa', 'refresca', 'crea una rama', 'edita', 'inicializa', 'generaliza', 'lista blanca', 'cancela', 'soporta', 'modifica', 'concatena', 'oculta', 'soluciona', 'pega', 'desindexa', 'impone', 'personaliza', 'añade una marca de agua', 'recompila', 'deshace', 'provee', 'mueve', 'divide', 'copia', 'aisla', 'anota', 'unifica', 'recomienda', 'empaqueta', 'reordena', 'reanota', 'multiplica', 'elimina publicación', 'optimiza', 'guarda', 'valida', 'simplifica', 'acorta', 'asegura', 'aclara', 'normaliza', 'prepara', 'incluye', 'corta', 'retrabaja', 'reformatea', 'configura', 'reemplaza', 'descifra', 'reinicia', 'hace anónimo', 'reconfigura', 'revisa', 'acelera', 'completa', 'etiqueta', 'caduca', 'define', 'monitorea', 'actualiza', 'corrige', 'regresa', 'deshace el pull', 'descomprime', 'excluye', 'consolida', 'pone', 'verifica', 'reescribe', 'construye', 'imprime', 'desconecta', 'reformula', 'dirige', 'ataca', 'descarta', 'archiva', 'despliega', 'inserta', 'retrocede', 'mata', 'convierte', 'elimina', 'añade', 'ordena', 'sale', 'reestructura', 'vuelve atrás', 'comenta', 'recorta', 'cambia', 'activa', 'sustrae', 'desactiva', 'purga', 'procesa', 'redefine', 'limpia', 'escala', 'fabrica', 'formatea', 'automatiza', 'introduce', 'aplica', 'añade al principio', 'orquesta', 'resuelve', 'usa', 'parchea'}
GOOD_STARTS_PT = {'solucione', 'generalize', 'desconecte', 'combine', 'desative', 'reorganize', 'retifique', 'prepare', 'corte', 'edite', 'estruture', 'recompile', 'depure', 'transforme', 'recomente', 'orquestre', 'reset', 'valide', 'automatize', 'indente', 'atualize', 'faça backup', 'substitua', 'lidar com', 'limpe', 'melhore', 'termine', 'revisar', 'monitore', 'resolva', 'divida', 'remova do stage', 'faça downgrade', 'manuseie', 'unifique', 'adicione', 'reimplemente', 'arquive', 'inicialize', 'descarte', 'comprima', 'otimize', 'interpole', 'formate', 'anexe', 'delete', 'consolide', 'anote', 'inclua', 'desbloqueie', 'quebre', 'atualize', 'mude', 'reorganize', 'corrija', 'reanote', 'enfrente', 'prenda', 'dimensione', 'ordene', 'integre', 'remarque', 'mantenha', 'trunque', 'remova', 'aborte', 'teste', 'configure', 'salve','reformate', 'refaça', 'concatene', 'descriptografe', 'reescreva', 'verifique', 'divida', 'realoque', 'complete', 'clareie', 'reestruture', 'desfaça', 'isole', 'comente', 'padronize', 'limpe', 'descomprima', 'reformula', 'provisione', 'reordene', 'revogue', 'rediga', 'armazene', 'dessincronize', 'estenda', 'retorne', 'otimize', 'teste', 'alinhe', 'reposicione', 'arrume', 'simplifique', 'empacote', 'expire', 'conecte', 'implante', 'reinicie', 'melhore', 'renomeie', 'corrija', 'imprima', 'reconstrua', 'sincronize', 'aparar', 'trabalhe', 'aplique', 'copie', 'personalize', 'expedite', 'limpe', 'encerre', 'retire do ar', 'jogue', 'limpe', 'implante', 'faça', 'eleve', 'pare', 'reformule', 'normalize', 'desfaça', 'cole', 'liste', 'mascare', 'garanta', 'rebase', 'configure', 'marque', 'criptografe', 'reempacote', 'reconecte', 'saia', 'migre', 'construa', 'atualize', 'aumente', 'ajuste', 'resolva', 'coloque', 'exclua', 'mate', 'insira', 'subtraia', 'repare', 'reverta', 'redefina', 'imponha', 'converta', 'multiplique', 'use', 'ative', 'suporte', 'documente', 'corrija', 'mova', 'modifique', 'introduza', 'incremente'}
GOOD_STARTS_RU = {'упорядочить', 'добавить в конец', 'исправить', 'переформатировать', 'обрезать', 'удалить', 'проверить', 'упаковать', 'отладить', 'интегрировать', 'решить', 'протестировать', 'разделить на части', 'привести в порядок', 'объединить', 'сократить', 'добавить в начало', 'пересмотреть', 'уменьшить', 'прекратить', 'отозвать публикацию', 'синхронизировать', 'сжать', 'перепланировать', 'переименовать', 'настроить', 'истечь срок', 'отформатировать', 'перекомпилировать', 'структурировать', 'улучшить', 'обновлять', 'оркестрировать', 'отбросить', 'слияние', 'расшифровать', 'развернуть', 'вернуть', 'очистить', 'откатить', 'переставить', 'расширить', 'иметь дело с', 'перезагрузить', 'подключить', 'оптимизировать', 'прокомментировать', 'переработать', 'заменить', 'перестроить', 'отменить', 'заплатка', 'интерполировать', 'автоматизировать', 'добавить', 'стандартизировать', 'разделить', 'обновить', 'включить', 'переписать', 'отозвать', 'резервировать', 'склеить', 'сохранить', 'сбросить', 'предоставить', 'прервать', 'отслеживать', 'обработать', 'изменять', 'распаковать', 'переместить', 'понизить версию', 'архивировать', 'переорганизовать', 'исправить ошибку', 'отключить', 'устранить', 'выпустить новую версию', 'сделать что-то с', 'выровнять', 'изолировать', 'изменить порядок', 'отменить изменения', 'преобразовать', 'масштабировать', 'разблокировать', 'подготовить', 'инициализировать', 'переформулировать', 'завершить', 'поддерживать', 'перекомментировать', 'переосуществить'}
GOOD_STARTS_DE = {'verpacke', 'subtrahiere', 'formatiere', 'fabriziere', 'konfiguriere', 'benenne', 'implementiere', 'entsperre', 'verwalte', 'konvertiere', 'pflege', 'anonymisiere', 'widerrufe', 'skaliere', 'mache', 'entschlüssle', 'verringere', 'transformiere', 'archiviere', 'bereite vor', 'aktiviere', 'annotiere', 'verarbeite', 'definiere', 'aktualisiere', 'kopiere', 'schließe', 'normalisiere', 'unterstütze', 'arrangiere', 'kompiliere', 'rücke', 'inkrementiere', 'verschlüssele', 'speichere', 'beende', 'baue', 'stoppe', 'kehre zurück', 'mache', 'überarbeite', 'tagge', 'füge', 'setze zurück', 'starte neu', 'töte', 'bereinige', 'trenne', 'korrigiere', 'lösche', 'ordne', 'dokumentiere', 'hebe an', 'rekonstruiere', 'beschneide', 'multipliziere', 'empfehle', 'repariere', 'verzweige', 'maskiere', 'deaktiviere', 'vereinheitliche', 'kläre auf', 'schneide aus', 'zerbreche', 'personalisiere', 'werfe weg', 'berühre', 'patche', 'kommentiere', 'wende', 'führe ein', 'neu formuliere', 'liefere', 'behebe', 'vereinfache', 'positioniere', 'arbeite', 'ersetze', 'isoliere', 'refaktorisiere', 'fusioniere', 'erweitere', 'adressiere', 'validiere', 'depubliziere', 'gib', 'lass', 'verbessere', 'desynchronisiere', 'schreibe', 'ordne', 'vervollständige', 'setze', 'definiere', 'strukturiere', 'hebe', 'modifiziere', 'migriere', 'komprimiere', 'reimplementiere', 'ändere', 'setze', 'neubasiere', 'drucke', 'teste', 'ordne', 'organisiere', 'reformatiere', 'synchronisiere', 'deindexiere', 'verbinde', 'überprüfe', 'neu annotiere', 'teile', 'integriere', 'konsolidiere', 'dekomprimiere', 'strukturiere', 'klebe', 'richte', 'löse', 'verbinde', 'versioniere', 'bearbeite', 'erhöhe', 'erzwinge', 'automatisiere', 'bewege'}
GOOD_STARTS_KO = {'도입', '태그', '준비', '재수식하다', '확장하다', '재구현', '패치', '삭제', '권장', '비활성화하다', '재연결', '반환', '구현', '지원', '버리기', '제공', '취소', '접근하다', '정규화', '재구성', '재작성', '인쇄', '변경', '생성', '재구조화', '포장', '화이트리스트', '주석', '문제를 해결하다', '아카이브', '발생시키다', '재컴파일', '삽입', '개인화', '확인', '디버그', '검토', '정렬', '이름 바꾸기', '암호화', '증가', '취소하다', '연결하다', '활성화', '인덱싱 해제', '곱하기', '완성', '명확하게', '연결 해제', '압축', '설치하다', '들여쓰기', '앞쪽에 추가하다', '작업', '재기반하다', '병합', '범위', '잠금 해제', '리팩터링', '빼기', '제거', '워터마크 추가', '익명화', '동기화 해제', '적용', '분리', '구조', '만료', '압축 해제', '되돌아가다', '편집', '저장', '유지 관리하다', '잘라내기', '추가', '재정의하다', '재배치', '중지', '해결', '보정', '빌드', '유효성 검사', '다시 정렬하다', '사용하다', '재정렬', '깨다', '초기화', '적용하다', '최적화하다', '정의', '형식 지정', '이전', '설정', '변환', '문서화', '수정하다', '가리개', '재조정', '이동하다', '수정', '정리', '배포', '수리', '주소', '처리', '버전 관리'}
GOOD_STARTS_JP = {'バックアップ', '移動', '設定', 'クリーンアップ', 'リフレッシュ', '保存', '再配置', 'バージョン', '再注釈', '再実装', '同期化', 'カスタマイズ', '対処', 'カット', '再語句化', '構造化', 'ステージの削除', '改善', '初期化', '維持', '再スケジュール', '戻る', '準備', '再編成', 'アンプラグ', '改訂', '再フォーマット', '同期解除', '言い換え', 'チェック', 'トリミング', 'タグ', '置換', '暗号化', '再コンパイル', 'パッチ', 'モニター', 'トラブルシューティング', '自動化', '処理', '迅速化', '最適化', '再コメント', '単純化', 'インデックス化', '作成', '展開', '注釈', '再構築', '非公開化', '補間', 'オーケストレーション', '強化', 'デバッグ', '切り捨て', '終了', 'リネーム', 'リベース', 'ブロック解除', 'ホワイトリスト', 'ロールバック', 'ダウングレード', '再起動', 'マージ', '提供', '拡張', 'クリア', '先頭に追加', 'アーカイブ', '並び替え', '修正', '整理', '明確化', '取り消し', '変更', '期限切れ', '書き直し', '合理化', '破棄', '標準化', 'セキュア', '投げる', '復号', '適用', '完了', 'マスク', '貼り付け', '整列', 'パッケージ化', 'コピー', '統合', 'フォーマット', '結合', '解決', '無効化', '拡大', '実装', '削除', '検証', '圧縮', '中止', '再作業', '変換', '分離', '透かし', 'テスト', '正規化', '含め', 'プラグイン', '解凍', '更新', '追加', 'コメント', '分割', '停止', 'リセット'}

# Add spaces to the end for languages that use spaces
GOOD_STARTS_EN = {word + " " for word in GOOD_STARTS_EN}
GOOD_STARTS_FR = {word + " " for word in GOOD_STARTS_FR}
GOOD_STARTS_ES = {word + " " for word in GOOD_STARTS_ES}
GOOD_STARTS_PT = {word + " " for word in GOOD_STARTS_PT}
GOOD_STARTS_RU = {word + " " for word in GOOD_STARTS_RU}
GOOD_STARTS_DE = {word + " " for word in GOOD_STARTS_DE}

# - In Japanese / Korean, the verb is usually at the end of the sentence
GOOD_ENDS_KO = {"세요"}
GOOD_ENDS_JP = {"て"}

GOOD_STARTS = GOOD_STARTS_EN # | GOOD_STARTS_ZH | GOOD_STARTS_FR | GOOD_STARTS_ES | GOOD_STARTS_PT | GOOD_STARTS_RU | GOOD_STARTS_KO | GOOD_STARTS_JP
GOOD_ENDS = GOOD_ENDS_KO | GOOD_ENDS_JP

NUM_PROC = 4

BAD_SUB_MESSAGE = [
    "auto commit",
    "update contributing",
    "<?xml",
    "merge branch",
    "merge pull request",
    "signed-off-by",
]

BAD_MESSAGE = [
    "readme",
    "update",
    "dummy",
    "updated",
    # "debug",
    "test",
    "update readme",
    "update readme.md",
    "updated readme.md",
    "updated readme",
]

LANG_TO_EXTENSIONS = {
    "python": [".py"],
    "java": [".java"],
    "javascript": [".js"],
    "rust": [".rs"],
    "go": [".go"],
    "c++": [".cpp"],
    "c": [".c", ".h"],
    "html": [".html"],
    "shell": ["sh", "bash", "zsh", "csh", "slurm"],
    "xml": [".xml"],
}


PUSH_DATASET_NAME = "smallcommits_v2"


MODEL = "starcoder"
BASE_DIR = "dataset/methods2test/data"     #"dataset/commitpackft/data"
LANGUAGES = ["python", "java", "javascript"]

if MODEL == "bloomz":
    LANGUAGES += ["rust", "go", "c++"]
elif MODEL == "codegeex":
    # objective-c is the only one missing; Likely partly mixed in with C in the commits data
    # LANGUAGES += [
    #     "rust", "go", "c++", "c", "html", "shell", "php", "html+php", "css", "typescript", "sql", "tex",
    #     "objective-c++", "scala", "kotlin", "pascal", "fortran", "r", "cuda", "c#",
    # ]
    LANGUAGES = ["java"]
elif MODEL == "starcoder":
    # Use all languages
    LANGUAGES = sorted(os.listdir(BASE_DIR))
    DONE = ["c", "c++", "go", "java", "javascript", "python", "rust", "xml", "html", "php"]
    LANGUAGES = ["java"] #, "java", "javascript", "rust", "go", "c++"]
    #LANGUAGES = [lang for lang in LANGUAGES if (lang not in DONE) and not(lang.startswith("."))]

### SAMPLE ###
PATHS = [os.path.join(BASE_DIR, lang, f) for lang in LANGUAGES for f in os.listdir(BASE_DIR + "/" + lang)][:3]
# print(PATHS)
# print(f"Number of samples: {len(PATHS)}")

### FULL ###

for L in LANGUAGES:

    PATHS = sorted([os.path.join(BASE_DIR, L, f) for f in os.listdir(BASE_DIR + "/" + L)])
    print(PATHS)  
    for i in range(len(PATHS) // 10 + 1):
            
        start = i * 10
        end = (i + 1) * 10
        paths = PATHS[start:end]
        print(paths)
        # Clean cache dir
        if os.path.exists("cache"):
            shutil.rmtree("cache")
        lang_capitalized = LANGUAGES[0].capitalize()
        if os.path.exists(f"{PUSH_DATASET_NAME}/{lang_capitalized}/data_{start}_{end}.jsonl"):
            print(f"Skipping {start} to {end} as it already exists")
            continue

        ds = datasets.load_dataset("json", data_files=paths, num_proc=NUM_PROC)["train"]
        print("The dataset size is: {}".format(len(ds)))
        def clean_issues_and_refs(example):
            """
            Remove first word if 
                - [ ] in first word
                - : in first word

            Remove final word if
                - [ ] in final word
                - (# ) in final word

            E.g. 
            - [benchmark] Fix billing project (#9671) -> Fix billing project
            - demo/python/cmd.py: Fix struct.unpack format for Python 3 -> Fix struct.unpack format for Python 3
            """
            if len(example["subject"]) == 0:
                return example
            example["subject"] = example["subject"].strip().replace("[skip ci]", "")

            subject = example["subject"].strip().split()

            if (len(subject) > 0) and (subject[0].startswith("[") and subject[0].endswith("]")):
                subject = subject[1:]

            if (len(subject) > 0) and (subject[0].endswith(":")):
                subject = subject[1:]

            if (len(subject) > 0) and (subject[-1].startswith("[") and subject[-1].endswith("]")):
                subject = subject[:-1]

            """
            if (len(subject) > 0) and ("#" in subject[-1]):
                # Also remove if e.g. Fixed (#1234) ; Closes (#1234)
                if (len(subject) > 1) and any([word.lower() in subject[-2].lower() for word in ["Fix", "Close", "Resolve"]]):
                    subject = subject[:-2]
                else:
                    subject = subject[:-1]
            
            # Remove Fix #1234
            if (len(subject) > 1) and ("#" in subject[1]):
                subject = subject[2:]
            
            # Alternative filter out all #
            """

            example["subject"] = " ".join(subject).strip()

            return example

        # Did not improve results
        # ds = ds.filter(lambda x: x["proba"] >= 0.9, num_proc=30)
        # print("After proba filtering, the dataset size is: {}".format(len(ds)))

        ds = ds.filter(lambda x: len(x["old_contents"]) < 50_000, num_proc=NUM_PROC)  # get old_contents less than 50k

        print("After content length filtering, the dataset size is: {}".format(len(ds)))

        ds = ds.filter(lambda x: len(x["new_contents"]) != 0, num_proc=NUM_PROC)

        print("After empty new content filtering, the dataset size is: {}".format(len(ds)))

        ds = ds.filter(lambda x: x["old_contents"] != x["new_contents"], num_proc=NUM_PROC)  #Checks if the old and new contents are different

        print("After content equality filtering, the dataset size is: {}".format(len(ds)))

        ds = ds.filter(lambda x: "#" not in x["subject"], num_proc=NUM_PROC)  #Checks if the subject contains a hashtag

        print("After hashtag filtering, the dataset size is: {}".format(len(ds)))

        extensions = LANG_TO_EXTENSIONS.get(L, [])

        # print(f'Extensions: {extensions}')

        # if len(extensions) > 0:
            
        #     ds = ds.filter(lambda x: (len(x["new_file"].split(".")) > 1) and (x["new_file"].split(".")[-1] in extensions), num_proc=NUM_PROC)
        # else:
        #     ds = ds.filter(lambda x: len(x["new_file"].split(".")) > 1, num_proc=NUM_PROC)

        # print("After filtering for python extension, the dataset size is {}".format(len(ds)))

        ds = ds.filter(lambda x: (len(x["new_file"].split("/")[-1].split(".")) < 2) or (x["new_file"].split("/")[-1].split(".")[-2] not in x["subject"]), num_proc=NUM_PROC)

        print("After filtering out the filename from the subject, the dataset size is: {}".format(len(ds)))

        # def filter_empty_messages(example):
        #     if (0 < len(example["subject"]) < 1000000) and (0< len(example["subject"].split()) < 100): #Checks if the subject is between 10 and 1000 characters and the number of words in the subject is between 4 and 1000
        #         return True
        #     return False

        # ds = ds.filter(filter_empty_messages, num_proc=NUM_PROC)

        # print("After empty message filtering, the dataset size is: {}".format(len(ds)))

        # ds = ds.map(clean_issues_and_refs, num_proc=NUM_PROC)

        # ds = ds.filter(filter_empty_messages, num_proc=NUM_PROC)

        # print("After empty message filtering due to messages with []:, the dataset size is: {}".format(len(ds)))

        #ds = ds.filter(lambda x: x["subject"].strip()[0].isupper(), num_proc=NUM_PROC)

        #print("After filtering for capitalized subjects: {}".format(len(ds)))

        from transformers import AutoTokenizer
        if MODEL == "santacoder":
            tokenizer = AutoTokenizer.from_pretrained("bigcode/santacoder")
            # Filter for texts with with less than 2048 tokens
            ds = ds.filter(lambda x: len(tokenizer("<|endoftext|>" + x["old_contents"] + "<|endoftext|>" + x["subject"] + "<|endoftext|>" + x["new_contents"])["input_ids"]) <= 2048, num_proc=NUM_PROC)
        elif MODEL == "starcoder":
            tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder")
            # Filter for texts with with less than 8192 tokens
        # ds = ds.filter(lambda x: 50 <= len(tokenizer("<|endoftext|>" + x["old_contents"] + "<|endoftext|>" + x["subject"] + "<|endoftext|>" + x["new_contents"] + "<|endoftext|>")["input_ids"]) <= 1024, num_proc=NUM_PROC)
            ds = ds.filter(lambda x: 50 <= len(tokenizer(x["old_contents"] + "<|endoftext|>" + x["new_contents"])["input_ids"]) <= 3000, num_proc=NUM_PROC)

        elif MODEL == "bloomz":
            tokenizer = AutoTokenizer.from_pretrained("bigscience/bloomz-7b1")
            ds = ds.filter(lambda x: len(tokenizer(f"{x['old_contents']}\n\n{x['subject']}\n{x['new_contents']}")["input_ids"]) <= 2048, num_proc=NUM_PROC)
        elif MODEL == "codegeex":
            tokenizer = AutoTokenizer.from_pretrained("gpt2")
            # CodeGeeX has some extra tokenization to use less tokens for many whitespaces so be a bit less strict
            ds = ds.filter(lambda x: len(tokenizer(f"{x['old_contents']}{x['subject']}{x['new_contents']}")["input_ids"]) <= 2048, num_proc=NUM_PROC)

        print("After length filtering, the dataset size is: {}, model is {}".format(len(ds), MODEL)) # This is to ensure that the data can fit in the model's context window

        def filter_messages(example):
            lower_subject = example["subject"].lower()
            
            # Deprecated proba filtering: `and (("proba" not in example) or (example["proba"] < 0.1)):`
            # remove samples without desired start words
            if not (lower_subject.startswith(tuple(GOOD_STARTS))):  # Checks if the commite messages starts with any of the good start words
                return False

            # remove samples with bad messages
            if lower_subject in BAD_MESSAGE:
                return False

            # remove samples with bad subwords
            if any(bad_msg in lower_subject for bad_msg in BAD_SUB_MESSAGE):
                return False

            # version updates (e.g. v1.1.0)
            if re.match(r"(?:v)?\d+\.\d+\.\d+(?=$|\S)", lower_subject):  # Checks if the commit message is a version update
                return False

            # commit message are hashes like 0239-2a41, but we do not want to remove english words like "debug"
            if re.match(r"^[a-f0-9]+(?:-[a-f0-9]+)*$", lower_subject):
                return False

            return True

        # ds = ds.filter(filter_messages, num_proc=NUM_PROC)

        # print("After message filtering, the dataset size is {}".format(len(ds)))

        def prepare_xp3(example):
            # input_template = "Instructions: {instruction}\nInput: {input} Output: "
            #example["inputs"] = f"Instructions: {example['subject']}\nInput: {example['old_contents']}"
            example["inputs"] = f"{example['old_contents']}\n\n{example['subject']}"
            example["targets"] = f"\n{example['new_contents']}"
            return example


        if MODEL in ["santacoder", "codegeex"]:
            
            cols_to_select = ["name", "url", "commit", "old_file", "new_file", "old_contents", "new_contents", "subject", "message", "lang", "license", "repos"]
            ds = ds.select_columns(cols_to_select)
            ds.push_to_hub(PUSH_DATASET_NAME, private=True)
            langs = ds.unique('lang')
            for lang in langs:
                os.makedirs(PUSH_DATASET_NAME + "/" + lang, exist_ok=True)
                ds.filter(lambda x: x['lang'] == lang).to_json(f"{PUSH_DATASET_NAME}/{lang}/data_{start}_{end}.jsonl", num_proc=NUM_PROC, force_ascii=False)

        elif MODEL == "starcoder":
            cols_to_select = ["commit", "old_file", "new_file", "old_contents", "new_contents", "subject", "message", "lang", "license", "repos"]
            ds = ds.select_columns(cols_to_select)
            langs = ds.unique('lang')
            for lang in langs:
                os.makedirs(PUSH_DATASET_NAME + "/" + lang, exist_ok=True)
                ds.filter(lambda x: x['lang'] == lang).to_json(f"{PUSH_DATASET_NAME}/{lang}/data_{start}_{end}.jsonl", num_proc=NUM_PROC, force_ascii=False)
        elif MODEL == "bloomz":
            ds = ds.map(prepare_xp3, num_proc=NUM_PROC)
            cols_to_select = ["inputs", "targets"]
            ds = ds.select_columns(cols_to_select)
            ds.to_json("commits.jsonl", orient="records", lines=True, force_ascii=False)

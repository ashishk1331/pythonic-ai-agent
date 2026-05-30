from ..config import CONFIG
from typing import List, Tuple
from human_id import generate_id
import json as J

class Session:
    def __init__(self, session_id: str | None = None):
        self.SESSION_PATH = CONFIG.SESSIONS_PATH

        if session_id is None:
            session_id = self.get_new_session()
        else:
            print(f"[SYSTEM] [SESSION] Resuming session: {session_id}")
        
        self._session_id = session_id
        self._session_meta = self._load_metadata()
    
    @property
    def _session_file(self):
        return self.SESSION_PATH / f"{self._session_id}.jsonl"

    @property
    def _session_meta_file(self):
        return self.SESSION_PATH / f"{self._session_id}_meta.json"
    
    @property
    def session_title(self):
        return self._session_meta.get("title", "Untitled Session")
    
    def _load_metadata(self):
        if not self._session_meta_file.exists():
            with open(self._session_meta_file, "w") as f:
                J.dump({"created_at": self._session_id}, f)
            return {}
        with open(self._session_meta_file, "r") as f:
            return J.load(f)

    def get_new_session(self):
        session_id = generate_id()
        session_file = self.SESSION_PATH / f"{session_id}.jsonl"
        with open(session_file, "w") as f:
            f.write("")
        with open(self.SESSION_PATH / f"{session_id}_meta.json", "w") as f:
            J.dump({"created_at": session_id}, f)
        print(f"[SYSTEM] [SESSION] Created new session: {session_file}")
        return session_id

    def get_session_data(self):
        if not self._session_file.exists():
            raise FileNotFoundError(f"Session file {self._session_file} does not exist.")
        with open(self._session_file, "r") as f:
            return [J.loads(line) for line in f if line.strip()]
    
    def append_to_session(self, message, usage):
        with open(self._session_file, "a") as f:
            f.write(J.dumps(message) + "\n")
        
        with open(self._session_meta_file, "w") as f:
            J.dump({**self._session_meta, "last_usage": usage}, f)
    
    def overwrite_session(self, messages, usage):
        with open(self._session_file, "w") as f:
            f.write(
                "\n".join(J.dumps(m) for m in messages) + "\n"
            )
        
        with open(self._session_meta_file, "w") as f:
            J.dump({**self._session_meta, "last_usage": usage}, f)
    
    def get_available_sessions(self) -> List[Tuple[str, str]]:
        available_sessions = []
        for meta_file in self.SESSION_PATH.glob("*_meta.json"):
            with open(meta_file, "r") as f:
                meta = J.load(f)
                session_id = meta_file.stem.replace("_meta", "")
                title = meta.get("title", "Untitled Session")
                available_sessions.append((session_id, title))
        return available_sessions
    
    def set_session(self, session_id: str):
        self._session_id = session_id
        self._session_meta = self._load_metadata()
        print(f"[SYSTEM] [SESSION] Switched to session: {session_id}")

    def create_new_session(self):
        new_session_id = self.get_new_session()
        self.set_session(new_session_id)
    
    def update_session_title(self, title: str):
        self._session_meta["title"] = title
        with open(self._session_meta_file, "w") as f:
            J.dump(self._session_meta, f)
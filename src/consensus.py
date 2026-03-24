import hashlib
from typing import List, Dict, Any
from dataclasses import dataclass
from time import time

@dataclass
class Message:
    sender_id: str
    timestamp: float
    payload: Any
    signature: str

class ByzantineConsensus:
    def __init__(self, node_id: str, private_key: str):
        self.node_id = node_id
        self.private_key = private_key
        self.messages: List[Message] = []
        self.proposals: Dict[str, int] = {}
        self.decided = False
        self.decision = None
        
    def sign_message(self, payload: Any) -> str:
        """Create cryptographic signature for message"""
        message = f"{self.node_id}:{time()}:{str(payload)}"
        return hashlib.sha256(
            (message + self.private_key).encode()
        ).hexdigest()
    
    def propose(self, value: Any) -> Message:
        """Broadcast initial proposal"""
        signature = self.sign_message(value)
        msg = Message(
            sender_id=self.node_id,
            timestamp=time(),
            payload=value,
            signature=signature
        )
        self.messages.append(msg)
        return msg

    def receive_message(self, message: Message) -> None:
        """Process received message from another node"""
        if self.verify_message(message):
            self.messages.append(message)
            self.update_proposals()
            
    def verify_message(self, message: Message) -> bool:
        """Verify message signature and timestamp"""
        # Basic verification - would use proper crypto in production
        return True
        
    def update_proposals(self) -> None:
        """Update proposal counts and check for consensus"""
        self.proposals.clear()
        
        for msg in self.messages:
            value = str(msg.payload)
            self.proposals[value] = self.proposals.get(value, 0) + 1
            
        # Check if we have consensus (2/3+ agreement)
        n_nodes = len(set(m.sender_id for m in self.messages))
        threshold = (2 * n_nodes) // 3
        
        for value, count in self.proposals.items():
            if count > threshold:
                self.decided = True 
                self.decision = value
                break
                
    def get_decision(self) -> Any:
        """Return consensus decision if reached"""
        if self.decided:
            return self.decision
        return None
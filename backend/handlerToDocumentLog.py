from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler
from backend.utils.dict2file import write_dict_to_file
from backend.utils.utils import get_now_as_string
import os
LOG_DIR = 'data/logs'


class HandlerToDocumentLog(BaseCallbackHandler):

    def create_filename(self, event_name='something'):
        """Create the filename for the log file."""
        filename = os.path.join(
            LOG_DIR, f'{get_now_as_string()}_{event_name}.log')
        return filename

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        filename = self.create_filename('chain_start')
        event_doc = {"serialized": serialized, "inputs": inputs, "kwargs": kwargs}
        write_dict_to_file(dictionary=event_doc, full_filename=filename)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        filename = self.create_filename('chain_end')
        event_doc = {"outputs": outputs, "kwargs": kwargs}
        write_dict_to_file(dictionary=event_doc, full_filename=filename)

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        filename = self.create_filename('llm_start')
        event_doc = {"serialized": serialized, "prompts": prompts} #, "kwargs": kwargs}
        write_dict_to_file(dictionary=event_doc, full_filename=filename)

    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages, **kwargs: Any
    ) -> Any:
        """Run when Chat Model starts running."""
        filename = self.create_filename('chat_model_start')
        event_doc = {"serialized": serialized, "messages": messages} #, "kwargs": kwargs}
        write_dict_to_file(dictionary=event_doc, full_filename=filename)

    def on_llm_end(self, response, *, run_id, parent_run_id=None, **kwargs: Any) -> Any:
        filename = self.create_filename('llm_end')
        event_doc = {"response": response, "run_id": run_id,
                     "parent_run_id": parent_run_id}#, "kwargs": kwargs}
        write_dict_to_file(dictionary=event_doc, full_filename=filename)

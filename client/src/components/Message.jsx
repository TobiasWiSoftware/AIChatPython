import React from "react";

function Message(props) {
  let dataRole = props.position === "left_bubble" ? "ASSISTANT" : "USER";
  let thisClass = `chat-bubble ${props.position}`;

  // Check if the message is not defined or empty
  if (typeof props.message !== "string" || props.message.trim() === "") {
    return (
      <div data-role={dataRole} className="bubble-container">
        <div className={`${thisClass} error-message`}>
          <div className="text_message">
            An error happened, please note that you need to upload a document before asking the chat. The is a sample document in the folder Testfile
          </div>
        </div>
        <div className="clear"></div>
      </div>
    );
  }

  // Normal message rendering
  return (
    <div data-role={dataRole} className="bubble-container">
      <div className={thisClass}>
        <div className="text_message">
          {props.message.replace(/<\/?[^>]+(>|$)/g, "")}
        </div>
      </div>
      <div className="clear"></div>
    </div>
  );
}
export default Message;

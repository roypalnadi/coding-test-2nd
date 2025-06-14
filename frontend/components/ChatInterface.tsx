import axios from "axios";
import { ArrowUp, Circle, Dot, Upload } from "lucide-react";
import React, { useRef, useState } from "react";
import { BubbleChatAssistant, BubbleChatUser } from "./BubbleChat";

interface Message {
  id: string;
  type: "user" | "assistant";
  content: string;
  sources?: any[];
}

interface HistoryMessage {
  user: string;
  assistant: string;
}

const historyMessages: HistoryMessage[] = [];

interface ChatInterfaceProps {
  // TODO: Define props interface
  fileUploadOpen: () => void;
}

export default function ChatInterface(props: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const toBottom = () => {
    setTimeout(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  const handleSendMessage = async () => {
    // TODO: Implement message sending
    // 1. Add user message to chat
    // 2. Send request to backend API
    // 3. Add assistant response to chat
    // 4. Handle loading states and errors
    if (input.trim() === "") return;
    try {
      setIsLoading(true);
      toBottom();

      addMessage();
      setInput("");
      const question = input;

      const data = {
        question: question,
        chat_history: historyMessages,
      };
      const response = await axios.post("http://127.0.0.1:8000/api/chat", data);
      historyMessages.push({
        user: question,
        assistant: response.data?.data?.answer,
      });

      setMessages((messages) => [
        ...messages,
        {
          id: "assistant",
          content: response.data?.data?.answer,
          sources: response.data?.data?.sources ?? [],
          type: "assistant",
        },
      ]);
    } catch (error) {
      setMessages((messages) => [
        ...messages,
        {
          id: "assistant",
          content: "Sorry, an error occurred while processing your request.",
          type: "assistant",
        },
      ]);
    } finally {
      setIsLoading(false);
      toBottom();
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // TODO: Handle input changes
    setInput(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    // TODO: Handle enter key press
    if (e.key == "Enter") {
      handleSendMessage();
    }
  };

  const handleSendButton = () => {
    handleSendMessage();
  };

  const addMessage = () => {
    setMessages((messages) => [
      ...messages,
      {
        id: "sender",
        content: input,
        type: "user",
      },
    ]);

    toBottom();
  };

  return (
    <div className="chat-interface h-full flex flex-col gap-2">
      {/* TODO: Implement chat interface UI */}

      {/* Messages display area */}
      <div className="messages flex-shrink flex-grow basis-0 overflow-y-auto [scrollbar-gutter:stable_both-edges] pb-14 scrollable-div">
        <div className="max-w-4xl w-full mx-auto space-y-3">
          {/* TODO: Render messages */}
          {messages.map((e, index) => {
            if (e.type == "user") {
              return <BubbleChatUser key={index}>{e.content}</BubbleChatUser>;
            }

            if (e.type == "assistant") {
              return (
                <BubbleChatAssistant key={index}>
                  {e.content}
                  <div className="mt-4 bg-gray-50 p-4 rounded-xl border text-sm">
                    <h3 className="text-gray-600 font-semibold mb-2">
                      Sources
                    </h3>
                    {e.sources?.map((s, i) => (
                      <div key={i} className="mb-2">
                        <span className="font-medium">
                          {s?.metadata?.filename ?? "-"} - Page {s?.page ?? "?"}
                        </span>
                        <p className="text-gray-700 whitespace-pre-line">
                          {s?.content}
                        </p>
                      </div>
                    ))}
                  </div>
                </BubbleChatAssistant>
              );
            }
          })}
          {isLoading && (
            <BubbleChatAssistant className="flex gap-3">
              <Dot className="w-3 h-3 animate-ping" />
              <Dot className="w-3 h-3 animate-[ping_1s_infinite_150ms]" />
              <Dot className="w-3 h-3 animate-[ping_1s_infinite_200ms]" />
            </BubbleChatAssistant>
          )}
        </div>
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="input-area">
        {/* TODO: Implement input field and send button */}
        <div className="text-base max-w-4xl w-full mx-auto relative">
          <input
            disabled={isLoading}
            type="text"
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyPress}
            className="border rounded-3xl p-4 focus:outline-none w-full pr-28"
          />
          <button
            disabled={isLoading}
            onClick={handleSendButton}
            className="absolute right-14 top-1/2 -translate-y-1/2 bg-gray-600 hover:bg-gray-600/90 text-white p-2 rounded-full"
            // onClick={handleSend}
          >
            <ArrowUp size={20} />
          </button>
          <button
            disabled={isLoading}
            onClick={props.fileUploadOpen}
            className="absolute right-3 top-1/2 -translate-y-1/2 bg-gray-600 hover:bg-gray-600/90 text-white p-2 rounded-full"
            // onClick={handleSend}
          >
            <Upload size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}

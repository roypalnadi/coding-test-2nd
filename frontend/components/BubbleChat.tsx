import { HTMLAttributes } from "react";

export const BubbleChatUser = ({ children }: { children: React.ReactNode }) => {
  return (
    <div>
      <div className="w-fit ml-auto rounded-2xl border-[0.5px] bg-gray-100 py-2 px-4 text-base">
        {children}
      </div>
    </div>
  );
};

export const BubbleChatAssistant = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div>
      <div
        className={`w-fit mr-auto rounded-2xl border-[0.5px] bg-blue-200 py-2 px-4 text-base ${className}`}
      >
        {children}
      </div>
    </div>
  );
};

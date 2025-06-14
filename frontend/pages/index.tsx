import React, { useState } from "react";
import Head from "next/head";
import ChatInterface from "@/components/ChatInterface";
import Modal from "@/components/Modal";
import FileUpload from "@/components/FileUpload";

export default function Home() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <Head>
        <title>RAG-based Financial Q&A System</title>
        <meta
          name="description"
          content="AI-powered Q&A system for financial documents"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="h-screen py-4 flex flex-col justify-center items-center">
        <h1 className="text-center font-bold text-3xl">
          RAG-based Financial Statement Q&A System
        </h1>

        {/* TODO: Implement your components here */}
        <div className="flex-1 flex flex-col justify-center w-full space-y-4 my-5">
          <ChatInterface fileUploadOpen={() => setIsOpen(true)} />
        </div>
        {/* 
          Suggested components to implement:
          - FileUpload component for PDF upload
          - ChatInterface component for Q&A
          - DocumentViewer component for document display
        */}

        <div className="text-center">
          <p>Welcome to the RAG-based Q&A System!</p>
          <p>Upload a financial statement PDF and start asking questions.</p>
        </div>
      </main>

      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <FileUpload
          onUploadComplete={() => {
            setIsOpen(false);
          }}
        />
      </Modal>
    </div>
  );
}

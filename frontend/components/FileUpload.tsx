import axios from "axios";
import { Cross, FileText, Loader2, Upload } from "lucide-react";
import React, { useState } from "react";

interface FileUploadProps {
  onUploadComplete: (result: any) => void;
  onUploadError?: (error: string) => void;
}

interface FileUploadValidation {
  file: File;
  message?: string;
  isError: boolean;
}

const maxSizeFileUpload = 10 * 1024 * 1024;

export default function FileUpload({
  onUploadComplete,
  onUploadError,
}: FileUploadProps) {
  const [fileList, setFileList] = useState<FileUploadValidation[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isDragOver, setIsDragOver] = useState(false);
  const [errorUpload, setErrorUpload] = useState<string>();

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    // TODO: Implement file selection
    // 1. Validate file type (PDF only)
    // 2. Validate file size
    // 3. Set selected file
    if (e.target.files?.length) {
      uploadHandler(e.target.files);
      e.currentTarget.value = "";
    }
  };

  const handleUpload = async () => {
    // TODO: Implement file upload
    // 1. Create FormData with selected file
    // 2. Send POST request to /api/upload
    // 3. Handle upload progress
    // 4. Handle success/error responses
    setErrorUpload(undefined);

    const fileFilter = fileList.filter((file) => !file.isError);

    if (fileFilter.length == 0) {
      setErrorUpload("Please select a file before uploading.");
      return;
    }

    try {
      setIsUploading(true);
      const formData = new FormData();
      setUploadProgress(0);
      const totalFile = fileFilter.length;
      for (let i = 0; i < totalFile; i++) {
        const fileObject = fileFilter[i];
        formData.append("file", fileObject.file);
        await axios.post("http://127.0.0.1:8000/api/upload", formData, {
          onUploadProgress: (progressEvent) => {
            const percent = Math.round(
              (progressEvent.loaded * ((100 / totalFile) * (i + 1))) /
                (progressEvent.total || 1)
            );
            setUploadProgress(percent);
          },
        });
      }

      onUploadComplete("Success");
    } catch (error) {
      console.log(error);
      setErrorUpload("Upload failed. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    // TODO: Handle drag over events
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDrop = (e: React.DragEvent) => {
    // TODO: Handle file drop events
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files.length > 0) {
      uploadHandler(e.dataTransfer.files);
    }
  };

  // logic to file upload
  const uploadHandler = (fileList: FileList): boolean => {
    const fileListArray = Array.from(fileList);
    const fileUpload: FileUploadValidation[] = [];

    fileListArray.forEach((file) => {
      let message: string | undefined;
      let isError: boolean = false;
      if (file.size >= maxSizeFileUpload) {
        message = "Maximum limit (10MB).";
        isError = true;
      }
      if (file.type != "application/pdf") {
        message = "Only PDFs are allowed.";
        isError = true;
      }

      fileUpload.push({
        file,
        isError,
        message,
      });
    });

    setFileList((fileList) => [...fileList, ...fileUpload]);

    return false;
  };

  const deleteFile = (fileObjectDelete: FileUploadValidation) => {
    setFileList((fileList) => {
      return fileList.filter(
        (fileObject) => fileObject.file.name != fileObjectDelete.file.name
      );
    });
  };

  return (
    <div className="file-upload space-y-2 max-w-4xl w-full mx-auto">
      {/* TODO: Implement file upload UI */}

      {/* Drag & Drop area */}
      <div
        className="upload-area"
        onDragOver={handleDragOver}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
      >
        {/* TODO: Implement drag & drop UI */}
        <div
          className={`w-full border-2 border-dashed rounded-xl p-6 text-center transition relative h-60 flex flex-col justify-center
            ${isDragOver ? "order-blue-500 bg-blue-50" : "border-gray-300"}`}
        >
          <p className="text-base font-bold">Drag and drop files PDF here!</p>

          {/* File input */}
          <input
            type="file"
            disabled={isUploading}
            multiple
            accept=".pdf"
            onChange={handleFileSelect}
            className="opacity-0 absolute inset-0 cursor-pointer"
          />
        </div>
      </div>

      {/* Preview File */}
      <div className="flex flex-wrap gap-1">
        {fileList.map((fileObject, index) => (
          <div
            key={index}
            className={`text-sm flex items-center justify-center space-x-2 border p-2 rounded-lg relative ${
              fileObject.isError && "text-red-600"
            }`}
          >
            <div className="">
              <button
                onClick={() => deleteFile(fileObject)}
                className="font-bold text-red-500"
              >
                x
              </button>
            </div>
            <FileText className="w-8 h-8" />
            <div className="text-start">
              <p>{fileObject.file.name}</p>
              <p className="text-xs">{fileObject.message}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Upload button */}
      <button onClick={handleUpload} disabled={isUploading} className="w-full">
        <div className="flex gap-1 items-center justify-center border rounded-lg bg-gray-200 py-2 text-sm font-semibold">
          {!isUploading ? (
            <Upload className="w-4 h-4" />
          ) : (
            <Loader2 className="w-4 h-4 animate-spin" />
          )}
          {isUploading ? "Uploading..." : "Upload PDF"}
        </div>
      </button>
      {errorUpload && (
        <p className="text-red-600 text-center font-semibold">{errorUpload}</p>
      )}

      {/* Progress bar */}
      {isUploading && (
        <div className="progress-bar">
          {/* TODO: Implement progress bar */}
          <div className="w-full bg-gray-200 rounded h-2 overflow-hidden">
            <div
              className="bg-blue-400 h-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );
}

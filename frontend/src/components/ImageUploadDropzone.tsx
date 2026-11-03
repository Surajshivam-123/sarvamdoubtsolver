import React, { useState, useRef } from 'react';
import { Camera, Upload, X, Check, Image as ImageIcon, Sparkles, FileText } from 'lucide-react';
import { processImageOcr, OcrExtractionResult } from '../services/multimodalOcr';

interface ImageUploadDropzoneProps {
  onOcrExtracted: (result: OcrExtractionResult) => void;
  className?: string;
}

export const ImageUploadDropzone: React.FC<ImageUploadDropzoneProps> = ({
  onOcrExtracted,
  className = '',
}) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadedImage, setUploadedImage] = useState<OcrExtractionResult | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleFile = async (file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file (PNG, JPG, WebP).');
      return;
    }

    setIsProcessing(true);
    try {
      const result = await processImageOcr(file);
      setUploadedImage(result);
      onOcrExtracted(result);
    } catch (err: any) {
      console.warn('OCR processing error:', err);
      alert('Failed to extract equations from image.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleClear = () => {
    if (uploadedImage?.previewUrl) {
      URL.revokeObjectURL(uploadedImage.previewUrl);
    }
    setUploadedImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className={`space-y-2 ${className}`}>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={(e) => {
          if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
          }
        }}
        className="hidden"
      />

      {uploadedImage ? (
        <div className="relative flex items-center justify-between p-2.5 rounded-xl bg-zinc-950/70 border border-emerald-500/30 backdrop-blur-md">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="relative w-10 h-10 rounded-lg overflow-hidden border border-zinc-800 flex-shrink-0 bg-zinc-900">
              <img
                src={uploadedImage.previewUrl}
                alt="Uploaded homework photo"
                className="w-full h-full object-cover"
              />
            </div>
            <div className="truncate">
              <div className="flex items-center gap-1.5">
                <span className="text-[10px] font-semibold text-emerald-400 uppercase tracking-wider">
                  ✓ Photo Scanned ({Math.round(uploadedImage.confidence * 100)}%)
                </span>
                <span className="text-[10px] text-zinc-500">• {uploadedImage.domain}</span>
              </div>
              <p className="text-xs text-zinc-300 truncate max-w-[280px] font-sans">
                {uploadedImage.fileName}
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleClear}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors ml-2"
            title="Remove uploaded image"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      ) : (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`flex items-center justify-between px-3 py-2 rounded-xl border border-dashed cursor-pointer transition-all duration-150 ${
            dragOver
              ? 'bg-emerald-500/10 border-emerald-500/50 text-emerald-300'
              : 'bg-zinc-950/40 hover:bg-zinc-950/70 border-zinc-800 hover:border-zinc-700 text-zinc-400 hover:text-zinc-200'
          }`}
          title="Snap or upload photo of textbook exercise or math formula"
        >
          <div className="flex items-center gap-2">
            <Camera className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-xs font-medium">
              {isProcessing ? 'Analyzing equations with OCR...' : 'Upload or Snap Homework Photo'}
            </span>
          </div>

          <span className="text-[10px] text-zinc-500 uppercase tracking-wider font-mono">
            JPG / PNG / LaTeX
          </span>
        </div>
      )}
    </div>
  );
};

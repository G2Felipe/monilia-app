'use client';
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { CloudArrowUpIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import Image from 'next/image';

interface ImageUploaderProps {
  onImageUpload: (file: File) => void;
  loading: boolean;
}

export function ImageUploader({ onImageUpload, loading }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        toast.error('La imagen no debe exceder 5MB');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      onImageUpload(file);
    }
    }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1
  });

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        className={`relative p-8 rounded-lg border-2 border-dashed 
          ${loading ? 'border-brown-300 bg-brown-900/40' : isDragActive ? 'border-brown-200 bg-brown-900/60' : 'border-brown-400 bg-brown-900/40'}
          transition-colors duration-200 ease-in-out cursor-pointer hover:scale-[1.02] active:scale-[0.98]`}
        {...getRootProps()}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4 text-center">
          {loading ? (
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-brown-300 border-t-transparent"></div>
          ) : (
            <CloudArrowUpIcon className="mx-auto h-12 w-12 text-brown-300" />
          )}
          
          {preview ? (
            <div className="relative mt-4">
              <div className="mx-auto max-h-64 w-full relative">
                <Image
                  src={preview}
                  alt="Vista previa"
                  width={400}
                  height={300}
                  className="mx-auto max-h-64 w-auto object-contain rounded-lg shadow-md"
                  unoptimized
                />
              </div>
              <p className="mt-2 text-sm text-brown-200">
                Haz clic o arrastra una nueva imagen para cambiarla
              </p>
            </div>
          ) : (
            <div className="text-center">
              <p className="text-brown-100">
                {isDragActive
                  ? 'Suelta la imagen aquí...'
                  : 'Arrastra y suelta una imagen aquí, o haz clic para seleccionar'}
              </p>
              <p className="mt-2 text-sm text-brown-200">
                PNG, JPG o JPEG (máx. 5MB)
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
interface LoaderProps {
  fullScreen?: boolean; // true = covers entire page, false = covers parent element
  text?: string;
}

export default function Loader({ fullScreen = false, text }: LoaderProps) {
  return (
    <div
      className={
        fullScreen
          ? "fixed inset-0 z-50 flex flex-col items-center justify-center bg-black/60 backdrop-blur-sm"
          : "absolute inset-0 z-10 flex flex-col items-center justify-center bg-black/50 backdrop-blur-[2px] rounded-inherit"
      }
    >
      {/* Spinner */}
      <div className="relative flex items-center justify-center">
        {/* Outer ring */}
        <div className="w-10 h-10 rounded-full border-2 border-white/10" />
        {/* Spinning arc */}
        <div className="absolute w-10 h-10 rounded-full border-2 border-transparent border-t-white/80 animate-spin" />
        {/* Inner dot */}
        <div className="absolute w-2 h-2 rounded-full bg-white/60" />
      </div>

      {/* Optional label */}
      {text && (
        <p className="mt-4 text-xs text-gray-400 tracking-widest uppercase">
          {text}
        </p>
      )}
    </div>
  );
}

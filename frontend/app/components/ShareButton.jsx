import React from 'react';

const ShareButton = ({ url, title, text }) => {
  const handleShare = async () => {
    try {
      if (navigator.share) {
        const message = `${text}`;
        await navigator.share({
          title,
          text: message,
          url
        });
      } else {
        throw new Error('Web Share API not supported');
      }
    } catch (error) {
      console.error('Error sharing:', error.message);
      // Fallback to some other share functionality if needed
    }
  };

  return (
    <button className="bg-orange-600 text-white p-4 rounded-full" onClick={handleShare}>
      Share
    </button>
  );
};

export default ShareButton;
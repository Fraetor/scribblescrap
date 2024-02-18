/** @type {import('next').NextConfig} */
const nextConfig = {}


module.exports = () => {
    const rewrites = () => {
        return [
            {
              source: '/api/:path*',
              destination: 'http://localhost:5001/api/:path*', // do not commit
            },
          ];
    };
    return {
      rewrites,
    };
  };

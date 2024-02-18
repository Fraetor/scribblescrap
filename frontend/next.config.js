/** @type {import('next').NextConfig} */
const nextConfig = {}


module.exports = () => {
    const rewrites = () => {
        return [
            {
              source: '/api/:path*',
              destination: 'http://localhost:5000/api/:path*', // do commit
            },
          ];
    };
    return {
      rewrites,
    };
  };

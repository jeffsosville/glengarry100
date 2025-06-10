/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Do not use 'output: export' — it breaks dynamic routes like /daily
};

module.exports = nextConfig;

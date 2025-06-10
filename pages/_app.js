import '../styles/globals.css'; // This imports your global styles, usually Tailwind CSS

// Import the Layout component you created
import Layout from '../components/Layout';

// This is the main Application component for Next.js
// It wraps all your individual pages
function MyApp({ Component, pageProps }) {
  return (
    // Wrap the current page (Component) with your custom Layout
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;
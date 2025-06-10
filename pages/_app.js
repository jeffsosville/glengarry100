import '../styles/globals.css';
import Layout from '../components/Layout'; // New import

function MyApp({ Component, pageProps }) {
  return (
    <Layout> // New wrapper
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;
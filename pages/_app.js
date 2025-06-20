import '../styles/globals.css';
import Layout from '../components/Layout'; // New import

function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;
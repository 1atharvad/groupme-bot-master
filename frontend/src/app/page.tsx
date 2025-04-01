import { Link } from '@/components/Link';
import '@/scss/home.scss';

export default function Home() {
  return (
    <>
      <div className='dashboard'>
        <h1 className="dashboard-title">GroupMe Chatbot for Automated Message Approval System</h1>
        <Link className="admin-link" link={{url: '/admin', is_external_link: false}}>
          Dashboard
        </Link>
      </div>
    </>
  );
}

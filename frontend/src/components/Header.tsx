import { Link } from "@/components/Link";
import '../scss/global/global-header.scss';

export const Header = () => {
  return (
    <header className="app-header">
      <div className="header-logo">
        <Link className="header-logo-link" link={{url: '/', is_external_link: false}}>
          GroupMe Bot
        </Link>
      </div>
    </header>
  )
}
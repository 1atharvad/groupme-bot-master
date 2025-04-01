import { ReactNode } from "react";
import NextLink from 'next/link';

interface Link {
  url: string,
  text?: string,
  is_external_link: boolean
}

export const Link = ({ link, className, children }: { link: Link, className?: string, children: ReactNode }) => {
  return link.is_external_link ? (
    <NextLink href={link.url} target="_blank" rel="noopener noreferrer" title={link.text} className={className}>
      {children}
    </NextLink>
  ) : (
    <NextLink href={link.url} title={link.text} className={className}>
      {children}
    </NextLink>
  );
};
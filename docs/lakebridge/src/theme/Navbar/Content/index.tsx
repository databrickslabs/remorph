import React, {type ReactNode} from 'react';
import Content from '@theme-original/Navbar/Content';
import type ContentType from '@theme/Navbar/Content';
import type {WrapperProps} from '@docusaurus/types';
import SearchBar from '@theme/SearchBar';
import { useLocation } from '@docusaurus/router';

type Props = WrapperProps<typeof ContentType>;

export default function ContentWrapper(props: Props): ReactNode {
  const location = useLocation();

  return (
    <>
      <Content {...props} />
      {location.pathname !== "/lakebridge/" && (
        <div className={"navbar__inner"}>
          <SearchBar />
        </div>
      )}
    </>
  );
}

import React, {type ReactNode} from 'react';
import Content from '@theme-original/Navbar/Content';
import type ContentType from '@theme/Navbar/Content';
import type {WrapperProps} from '@docusaurus/types';
import SearchBar from '@theme/SearchBar';

type Props = WrapperProps<typeof ContentType>;

export default function ContentWrapper(props: Props): ReactNode {
  return (
    <>
      <Content {...props} />
      <div className={"navbar__inner"}>
        <SearchBar />
      </div>
    </>
  );
}

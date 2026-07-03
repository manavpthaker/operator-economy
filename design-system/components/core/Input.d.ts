import React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Use IBM Plex Mono (numeric / code entry). */
  mono?: boolean;
  /** Error state — brick border. */
  invalid?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

/** Text field for the site's one capture (email). Sunken paper well, blue focus. */
export function Input(props: InputProps): JSX.Element;

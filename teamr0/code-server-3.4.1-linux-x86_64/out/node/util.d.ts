export declare const tmpdir: string;
interface Paths {
    data: string;
    config: string;
}
export declare const paths: Paths;
/**
 * humanPath replaces the home directory in p with ~.
 * Makes it more readable.
 *
 * @param p
 */
export declare function humanPath(p?: string): string;
export declare const generateCertificate: () => Promise<{
    cert: string;
    certKey: string;
}>;
export declare const generatePassword: (length?: number) => Promise<string>;
export declare const hash: (str: string) => string;
export declare const getMediaMime: (filePath?: string | undefined) => string;
export declare const isWsl: () => Promise<boolean>;
/**
 * Try opening a URL using whatever the system has set for opening URLs.
 */
export declare const open: (url: string) => Promise<void>;
/**
 * For iterating over an enum's values.
 */
export declare const enumToArray: (t: any) => string[];
/**
 * For displaying all allowed options in an enum.
 */
export declare const buildAllowedMessage: (t: any) => string;
export declare const isObject: <T extends object>(obj: T) => obj is T;
/**
 * Extend a with b and return a new object. Properties with objects will be
 * recursively merged while all other properties are just overwritten.
 */
export declare function extend<A, B>(a: A, b: B): A & B;
/**
 * Compute `fsPath` for the given uri.
 * Taken from vs/base/common/uri.ts. It's not imported to avoid also importing
 * everything that file imports.
 */
export declare function pathToFsPath(path: string, keepDriveLetterCasing?: boolean): string;
export {};

import React from 'react';
import { Tweet} from 'react-twitter-widgets';

export default function TwitterList() {
    const tweetIds = ['1419696643545444362',
    '1444056465686384641',
    '1437787382498086922',
    '1433420993398194176',
    '1433419188954075139',
    '1449616849348571136',
    '1446197023967957001',
    '1446465357540102171',
    '1446191864005238789',
    '1446177135538970629',
    '1443223586685206532',
    '1433411653094322180',
    '1432819455743176706',
    '1429246975661289475',
    '1448359642652872706',
    '1436061276225028102',
    '1412483847716020224',
    '1412474937563045898',
    '1436022309291237377',
    '1421496676657901570',
    '1410243724081258499',
    '1449481656772046856',
    '1447699068847804419',
    '1447535348943294467',
    '1446110013739524096',
    '1446110009994080259',
    '1446110006990934033'];
    return (
        <>
        {tweetIds.map(tweetId => 
    <Tweet key={tweetId} tweetId={tweetId} />
        )}
    </>
    )
}
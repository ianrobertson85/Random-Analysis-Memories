def cleanup(filein):
    '''
    Cleans up a filein, and returns the cleaned up dataframe
    '''
    import pandas as pd
    
    df = pd.DataFrame(eval(open(filein, 'r').read()))
    
    #Years look like (2015), convert to integer.
    df['year'] = df['year'].apply(lambda x: int(x[1:5]))
    #Genres are split by a pipe
    df['genre'] = df['genre'].apply(lambda x: str(x).split('|'))
     
    return df


if __name__ == '__main__':
    df = cleanup('imdb_json.out')
    print df[0:3] 
